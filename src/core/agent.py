"""
FoxDot Agent - Main entry point for the agent module
Re-exports from streaming_agent and provides backward compatibility
"""

import os
from typing import Dict, Any, Optional, List

# Re-export streaming agent components
from .streaming_agent import (
    StreamingFoxDotAgent,
    StreamEvent,
    StreamEventType,
    ContextManager,
    ConversationTurn,
    create_streaming_agent
)

# Re-export other components
from .session import FoxDotSession, Layer, MusicState, ChatMessage
from .executor import FoxDotExecutor, ExecutionResult
from .functions import ALL_FUNCTION_DECLARATIONS, build_foxdot_code, execute_function
from .prompts import SYSTEM_PROMPT, get_system_prompt


class FoxDotAgent(StreamingFoxDotAgent):
    """
    Main FoxDot Agent class.
    Extends StreamingFoxDotAgent with sync-first interface.
    """
    
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        auto_execute: bool = True,
        include_thoughts: bool = True
    ):
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            auto_execute=auto_execute,
            include_thoughts=include_thoughts
        )


# Factory function
def create_agent(**kwargs) -> FoxDotAgent:
    """Create a FoxDot agent with the given configuration."""
    return FoxDotAgent(**kwargs)


__all__ = [
    'FoxDotAgent',
    'StreamingFoxDotAgent',
    'StreamEvent',
    'StreamEventType',
    'ContextManager',
    'ConversationTurn',
    'FoxDotSession',
    'Layer',
    'MusicState',
    'ChatMessage',
    'FoxDotExecutor',
    'ExecutionResult',
    'ALL_FUNCTION_DECLARATIONS',
    'SYSTEM_PROMPT',
    'create_agent',
    'create_streaming_agent',
]
