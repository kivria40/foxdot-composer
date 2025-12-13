"""
FoxDot Streaming Agent - Streaming responses with thinking and function calling
Supports real-time streaming, thought summaries, and context consolidation
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional, List, Generator, AsyncGenerator, Callable
from dataclasses import dataclass, field
from enum import Enum
import datetime

from google import genai
from google.genai import types


class StreamEventType(Enum):
    """Types of streaming events."""
    THINKING_START = "thinking_start"
    THINKING_CHUNK = "thinking_chunk"
    THINKING_END = "thinking_end"
    TEXT_START = "text_start"
    TEXT_CHUNK = "text_chunk"
    TEXT_END = "text_end"
    FUNCTION_CALL_START = "function_call_start"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESULT = "function_result"
    FUNCTION_CALL_END = "function_call_end"
    ERROR = "error"
    DONE = "done"


@dataclass
class StreamEvent:
    """A streaming event from the agent."""
    type: StreamEventType
    data: Any = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp
        }


@dataclass
class ConversationTurn:
    """A single turn in the conversation for context management."""
    role: str
    content: str
    thinking: Optional[str] = None
    function_calls: List[Dict] = field(default_factory=list)
    token_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


class ContextManager:
    """
    Manages conversation context and consolidates when window gets large.
    Implements intelligent summarization to maintain relevant context.
    """
    
    def __init__(
        self,
        max_tokens: int = 100000,  # Conservative limit for context
        consolidation_threshold: float = 0.7,  # Consolidate at 70% of max
        keep_recent_turns: int = 5  # Always keep last N turns verbatim
    ):
        self.max_tokens = max_tokens
        self.consolidation_threshold = consolidation_threshold
        self.keep_recent_turns = keep_recent_turns
        self.turns: List[ConversationTurn] = []
        self.consolidated_summary: Optional[str] = None
        self.total_tokens = 0
        
    def add_turn(self, turn: ConversationTurn):
        """Add a conversation turn."""
        self.turns.append(turn)
        self.total_tokens += turn.token_count
        
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token average)."""
        return len(text) // 4
    
    def needs_consolidation(self) -> bool:
        """Check if context needs consolidation."""
        return self.total_tokens > (self.max_tokens * self.consolidation_threshold)
    
    def get_consolidation_prompt(self) -> str:
        """Generate prompt to consolidate old context."""
        old_turns = self.turns[:-self.keep_recent_turns] if len(self.turns) > self.keep_recent_turns else []
        
        if not old_turns:
            return ""
        
        turn_texts = []
        for turn in old_turns:
            turn_texts.append(f"{turn.role}: {turn.content[:500]}...")
            if turn.function_calls:
                turn_texts.append(f"  [Functions called: {', '.join(fc.get('name', '') for fc in turn.function_calls)}]")
        
        return f"""Summarize the following conversation history into a concise summary that preserves:
1. Key musical decisions made (tempo, scale, instruments)
2. User preferences discovered
3. Current state of the composition
4. Any important context for future requests

Conversation:
{chr(10).join(turn_texts)}

Provide a brief summary (2-3 paragraphs max):"""
    
    def consolidate(self, summary: str):
        """Apply consolidation with the provided summary."""
        self.consolidated_summary = summary
        # Keep only recent turns
        self.turns = self.turns[-self.keep_recent_turns:]
        self.total_tokens = sum(t.token_count for t in self.turns) + self.estimate_tokens(summary)
    
    def get_context_for_prompt(self) -> str:
        """Get context string to include in prompt."""
        parts = []
        
        if self.consolidated_summary:
            parts.append(f"## Previous Conversation Summary\n{self.consolidated_summary}\n")
        
        if self.turns:
            parts.append("## Recent Conversation")
            for turn in self.turns[-self.keep_recent_turns:]:
                parts.append(f"**{turn.role.title()}**: {turn.content}")
                if turn.function_calls:
                    calls = ", ".join(fc.get('name', '') for fc in turn.function_calls)
                    parts.append(f"  *[Functions: {calls}]*")
        
        return "\n".join(parts)
    
    def clear(self):
        """Clear all context."""
        self.turns.clear()
        self.consolidated_summary = None
        self.total_tokens = 0


class StreamingFoxDotAgent:
    """
    Streaming FoxDot Agent with thinking support and context consolidation.
    
    Features:
    - Real-time streaming responses
    - Thinking/reasoning visibility
    - Function calling with streaming
    - Automatic context consolidation
    """
    
    # Import function declarations and other components
    from .functions import ALL_FUNCTION_DECLARATIONS
    from .prompts import SYSTEM_PROMPT
    
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        auto_execute: bool = True,
        include_thoughts: bool = True,
        thinking_budget: int = -1,  # -1 for dynamic thinking
        max_context_tokens: int = 100000
    ):
        """
        Initialize the streaming agent.
        
        Args:
            model_name: Gemini model to use
            api_key: Google API key
            auto_execute: Auto-execute FoxDot code
            include_thoughts: Include thought summaries
            thinking_budget: Token budget for thinking (-1 for dynamic)
            max_context_tokens: Max tokens before consolidation
        """
        self.model_name = model_name
        self.auto_execute = auto_execute
        self.include_thoughts = include_thoughts
        self.thinking_budget = thinking_budget
        
        # Initialize client
        api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        
        self.client = genai.Client(api_key=api_key)
        
        # Initialize components
        from .session import FoxDotSession
        from .executor import FoxDotExecutor
        
        self.session = FoxDotSession()
        self.executor = FoxDotExecutor()
        self.context_manager = ContextManager(max_tokens=max_context_tokens)
        
        # Configure tools
        self.tools = types.Tool(function_declarations=self.ALL_FUNCTION_DECLARATIONS)
        
        # Conversation contents for API
        self.contents: List[types.Content] = []
        
        # Callbacks
        self._on_function_call: Optional[Callable] = None
        self._on_function_result: Optional[Callable] = None
    
    def set_callbacks(
        self,
        on_function_call: Optional[Callable] = None,
        on_function_result: Optional[Callable] = None
    ):
        """Set callbacks for function events."""
        self._on_function_call = on_function_call
        self._on_function_result = on_function_result
    
    def _get_generation_config(self) -> types.GenerateContentConfig:
        """Get generation configuration."""
        from .prompts import get_system_prompt
        
        config = types.GenerateContentConfig(
            system_instruction=get_system_prompt(self.session),
            tools=[self.tools],
            temperature=0.7,
        )
        
        # Add thinking config if supported
        if self.include_thoughts:
            config.thinking_config = types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=self.thinking_budget
            )
        
        return config
    
    def _build_code_from_function(self, func_name: str, args: Dict[str, Any]) -> Optional[str]:
        """Build FoxDot code from a function call."""
        from .functions import build_foxdot_code
        return build_foxdot_code(func_name, args, self.session)
    
    def _execute_function(self, func_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function and return result."""
        from .functions import execute_function
        return execute_function(func_name, args, self.session, self.executor, self.auto_execute)
    
    async def chat_stream(self, user_message: str) -> AsyncGenerator[StreamEvent, None]:
        """
        Process a message with streaming responses.
        
        Yields StreamEvent objects for:
        - Thinking chunks
        - Text chunks
        - Function calls
        - Function results
        
        Args:
            user_message: User's message
            
        Yields:
            StreamEvent objects
        """
        # Check if context needs consolidation
        if self.context_manager.needs_consolidation():
            yield StreamEvent(StreamEventType.THINKING_START, "Consolidating context...")
            
            # Generate consolidation summary
            consolidation_prompt = self.context_manager.get_consolidation_prompt()
            summary_response = self.client.models.generate_content(
                model=self.model_name,
                contents=consolidation_prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            
            if summary_response.text:
                self.context_manager.consolidate(summary_response.text)
                
            yield StreamEvent(StreamEventType.THINKING_END, "Context consolidated")
        
        # Add user message
        self.session.add_chat_message("user", user_message)
        user_content = types.Content(role="user", parts=[types.Part(text=user_message)])
        self.contents.append(user_content)
        
        # Get config
        config = self._get_generation_config()
        
        # Track state
        function_calls_made = []
        full_thinking = ""
        full_response = ""
        is_thinking = False
        is_responding = False
        
        try:
            # Start streaming
            stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=self.contents,
                config=config
            )
            
            for chunk in stream:
                if not chunk.candidates or not chunk.candidates[0].content.parts:
                    continue
                
                for part in chunk.candidates[0].content.parts:
                    # Handle thinking parts
                    if hasattr(part, 'thought') and part.thought and part.text:
                        if not is_thinking:
                            is_thinking = True
                            yield StreamEvent(StreamEventType.THINKING_START)
                        
                        full_thinking += part.text
                        yield StreamEvent(StreamEventType.THINKING_CHUNK, part.text)
                    
                    # Handle function calls
                    elif part.function_call:
                        if is_thinking:
                            is_thinking = False
                            yield StreamEvent(StreamEventType.THINKING_END, full_thinking)
                        
                        func_name = part.function_call.name
                        func_args = dict(part.function_call.args)
                        
                        yield StreamEvent(StreamEventType.FUNCTION_CALL_START)
                        yield StreamEvent(StreamEventType.FUNCTION_CALL, {
                            "name": func_name,
                            "args": func_args
                        })
                        
                        if self._on_function_call:
                            self._on_function_call(func_name, func_args)
                        
                        # Execute function
                        result = self._execute_function(func_name, func_args)
                        function_calls_made.append({
                            "name": func_name,
                            "args": func_args,
                            "result": result
                        })
                        
                        yield StreamEvent(StreamEventType.FUNCTION_RESULT, {
                            "name": func_name,
                            "result": result
                        })
                        
                        if self._on_function_result:
                            self._on_function_result(func_name, result)
                        
                        yield StreamEvent(StreamEventType.FUNCTION_CALL_END)
                    
                    # Handle text response
                    elif part.text:
                        if is_thinking:
                            is_thinking = False
                            yield StreamEvent(StreamEventType.THINKING_END, full_thinking)
                        
                        if not is_responding:
                            is_responding = True
                            yield StreamEvent(StreamEventType.TEXT_START)
                        
                        full_response += part.text
                        yield StreamEvent(StreamEventType.TEXT_CHUNK, part.text)
            
            # End states
            if is_thinking:
                yield StreamEvent(StreamEventType.THINKING_END, full_thinking)
            
            if is_responding:
                yield StreamEvent(StreamEventType.TEXT_END, full_response)
            
            # Handle function responses and continue generation if needed
            if function_calls_made:
                # Add model response to contents
                model_content = types.Content(
                    role="model",
                    parts=[types.Part(text=full_response)] if full_response else []
                )
                
                # Add function call parts
                for fc in function_calls_made:
                    model_content.parts.append(
                        types.Part.from_function_response(
                            name=fc["name"],
                            response={"result": fc["result"]}
                        )
                    )
                
                self.contents.append(model_content)
                
                # Continue generation for post-function response
                async for event in self._continue_after_functions(config, function_calls_made):
                    yield event
            
            # Add to context manager
            turn = ConversationTurn(
                role="assistant",
                content=full_response,
                thinking=full_thinking if full_thinking else None,
                function_calls=function_calls_made,
                token_count=self.context_manager.estimate_tokens(full_response + full_thinking)
            )
            self.context_manager.add_turn(turn)
            
            # Add to session
            self.session.add_chat_message(
                "assistant",
                full_response,
                code_generated="\n".join(
                    fc["result"].get("code", "") for fc in function_calls_made if fc["result"].get("code")
                )
            )
            
            yield StreamEvent(StreamEventType.DONE, {
                "response": full_response,
                "thinking": full_thinking,
                "function_calls": function_calls_made
            })
            
        except Exception as e:
            yield StreamEvent(StreamEventType.ERROR, str(e))
    
    async def _continue_after_functions(
        self,
        config: types.GenerateContentConfig,
        function_calls: List[Dict]
    ) -> AsyncGenerator[StreamEvent, None]:
        """Continue generation after function calls."""
        # Build function response content
        response_parts = []
        for fc in function_calls:
            response_parts.append(
                types.Part.from_function_response(
                    name=fc["name"],
                    response={"result": fc["result"]}
                )
            )
        
        self.contents.append(types.Content(role="user", parts=response_parts))
        
        # Generate continuation
        try:
            stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=self.contents,
                config=config
            )
            
            is_responding = False
            continuation = ""
            
            for chunk in stream:
                if not chunk.candidates or not chunk.candidates[0].content.parts:
                    continue
                
                for part in chunk.candidates[0].content.parts:
                    if part.text and not (hasattr(part, 'thought') and part.thought):
                        if not is_responding:
                            is_responding = True
                            yield StreamEvent(StreamEventType.TEXT_START)
                        
                        continuation += part.text
                        yield StreamEvent(StreamEventType.TEXT_CHUNK, part.text)
            
            if is_responding:
                yield StreamEvent(StreamEventType.TEXT_END, continuation)
                
        except Exception as e:
            yield StreamEvent(StreamEventType.ERROR, f"Continuation error: {e}")
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Synchronous chat method (non-streaming).
        
        Args:
            user_message: User's message
            
        Returns:
            Dict with response, thinking, and function_calls
        """
        import asyncio
        
        async def collect_stream():
            result = {
                "response": "",
                "thinking": "",
                "function_calls": []
            }
            
            async for event in self.chat_stream(user_message):
                if event.type == StreamEventType.THINKING_CHUNK:
                    result["thinking"] += event.data or ""
                elif event.type == StreamEventType.TEXT_CHUNK:
                    result["response"] += event.data or ""
                elif event.type == StreamEventType.FUNCTION_CALL:
                    pass  # Handled in DONE
                elif event.type == StreamEventType.DONE:
                    result = event.data
                    break
            
            return result
        
        return asyncio.run(collect_stream())
    
    def stop_all_music(self):
        """Stop all music."""
        result = self.executor.stop_all()
        self.session.clear_all()
        return result
    
    def get_current_code(self) -> str:
        """Get current FoxDot code."""
        return self.session.generate_full_code()
    
    def get_session_state(self) -> Dict[str, Any]:
        """Get current session state."""
        return {
            "music_state": self.session.music_state.to_dict(),
            "context_tokens": self.context_manager.total_tokens,
            "conversation_turns": len(self.context_manager.turns),
            "has_consolidated": self.context_manager.consolidated_summary is not None
        }
    
    def clear_context(self):
        """Clear conversation context."""
        self.context_manager.clear()
        self.contents.clear()
    
    def save_session(self, filepath: str):
        """Save session."""
        self.session.save_session(filepath)
    
    def load_session(self, filepath: str):
        """Load session."""
        self.session = self.session.load_session(filepath)


# Synchronous wrapper for easier use
def create_streaming_agent(**kwargs) -> StreamingFoxDotAgent:
    """Create a streaming FoxDot agent."""
    return StreamingFoxDotAgent(**kwargs)
