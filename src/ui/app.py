"""
FoxDot Music Agent - Streamlit UI with Real-time Async Streaming
"""

import streamlit as st
import asyncio
import json
import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Page config
st.set_page_config(
    page_title="FoxDot AI Music Agent",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Models
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
]

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .assistant-message {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 85%;
        border-left: 4px solid #4fd1c5;
    }
    .thinking-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        border: 1px solid #4fd1c5;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.85rem;
        color: #81e6d9;
        max-height: 200px;
        overflow-y: auto;
    }
    .tool-call-box {
        background: linear-gradient(135deg, #2d2d44 0%, #1f1f30 100%);
        border: 1px solid #f6ad55;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .tool-name { color: #f6ad55; font-weight: bold; }
    .tool-result { color: #68d391; margin-top: 0.5rem; }
    .layer-item {
        background: rgba(79, 209, 197, 0.1);
        border-left: 3px solid #4fd1c5;
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        border-radius: 0 8px 8px 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# FOXDOT GLOBALS - Shared across all instances like the old working code
# ============================================================================
_foxdot_env = {}
_foxdot_initialized = False


def init_foxdot():
    """Initialize FoxDot globally (like the old working code)."""
    global _foxdot_env, _foxdot_initialized
    
    if _foxdot_initialized:
        return True
    
    try:
        # First, check if FoxDot can connect to SuperCollider
        import FoxDot
        from FoxDot import Clock, Scale, Root
        
        # Get all FoxDot exports
        _foxdot_env = {name: getattr(FoxDot, name) for name in dir(FoxDot) if not name.startswith('_')}
        _foxdot_env['Clock'] = Clock
        _foxdot_env['Scale'] = Scale
        _foxdot_env['Root'] = Root
        _foxdot_env['print'] = print
        
        _foxdot_initialized = True
        st.toast("✅ FoxDot initialized!", icon="🎹")
        st.info("⚠️ Make sure you ran `FoxDot.start` in SuperCollider!")
        return True
    except ImportError as e:
        st.error(f"FoxDot not installed: {e}")
        return False
    except Exception as e:
        st.error(f"Error initializing FoxDot: {e}\n\n**Make sure SuperCollider is running and you executed `FoxDot.start` in it!**")
        return False


def execute_foxdot_code(code: str) -> Dict[str, Any]:
    """Execute FoxDot code directly (like the old working code)."""
    global _foxdot_env, _foxdot_initialized
    
    if not _foxdot_initialized:
        if not init_foxdot():
            return {"success": False, "error": "FoxDot not initialized"}
    
    try:
        exec(code, _foxdot_env)
        return {"success": True, "code": code}
    except Exception as e:
        return {"success": False, "error": str(e), "code": code}


def stop_all_music():
    """Stop all FoxDot music."""
    global _foxdot_env
    if _foxdot_env and 'Clock' in _foxdot_env:
        _foxdot_env['Clock'].clear()
        return True
    return False


# ============================================================================
# SESSION STATE
# ============================================================================
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'music_state' not in st.session_state:
        st.session_state.music_state = {'bpm': 120, 'scale': 'major', 'root': 'C', 'layers': {}}
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.environ.get('GOOGLE_API_KEY', '')
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gemini-2.5-flash"
    if 'auto_execute' not in st.session_state:
        st.session_state.auto_execute = True
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'contents' not in st.session_state:
        st.session_state.contents = []


# ============================================================================
# FUNCTION DECLARATIONS FOR GEMINI
# ============================================================================
FUNCTION_DECLARATIONS = [
    {
        "name": "play_synth",
        "description": "Play a melodic synthesizer pattern",
        "parameters": {
            "type": "object",
            "properties": {
                "player": {"type": "string", "description": "Player name (p1-p9, b1-b4)"},
                "synth": {"type": "string", "description": "Synth name (pluck, bass, keys, piano, pads, blip, saw)"},
                "notes": {"type": "string", "description": "Notes as Python list, e.g. '[0, 2, 4, 7]'"},
                "dur": {"type": "string", "description": "Duration, e.g. '1' or '[1, 0.5, 0.5]'"},
                "amp": {"type": "number", "description": "Volume 0.0-1.0"},
                "oct": {"type": "integer", "description": "Octave 3-7"},
            },
            "required": ["player", "synth", "notes"]
        }
    },
    {
        "name": "play_drums",
        "description": "Play drum pattern. x=kick, o=snare, -=hihat, *=clap",
        "parameters": {
            "type": "object",
            "properties": {
                "player": {"type": "string", "description": "Player name (d1-d9)"},
                "pattern": {"type": "string", "description": "Pattern string e.g. 'x-o-x-o-'"},
                "dur": {"type": "string", "description": "Duration"},
                "amp": {"type": "number", "description": "Volume 0.0-1.0"},
            },
            "required": ["player", "pattern"]
        }
    },
    {
        "name": "set_tempo",
        "description": "Set tempo in BPM",
        "parameters": {
            "type": "object",
            "properties": {"bpm": {"type": "integer", "description": "Tempo 40-200"}},
            "required": ["bpm"]
        }
    },
    {
        "name": "set_scale",
        "description": "Set musical scale",
        "parameters": {
            "type": "object",
            "properties": {"scale": {"type": "string", "enum": ["major", "minor", "dorian", "pentatonic", "blues"]}},
            "required": ["scale"]
        }
    },
    {
        "name": "set_root",
        "description": "Set root note",
        "parameters": {
            "type": "object",
            "properties": {"root": {"type": "string", "enum": ["C", "D", "E", "F", "G", "A", "B"]}},
            "required": ["root"]
        }
    },
    {
        "name": "stop_player",
        "description": "Stop a specific player",
        "parameters": {
            "type": "object",
            "properties": {"player": {"type": "string"}},
            "required": ["player"]
        }
    },
    {
        "name": "stop_all",
        "description": "Stop all music",
        "parameters": {"type": "object", "properties": {}}
    },
]


def build_code_from_function(name: str, args: Dict) -> str:
    """Build FoxDot code from function call."""
    if name == "play_synth":
        player = args.get('player', 'p1')
        synth = args.get('synth', 'pluck')
        notes = args.get('notes', '[0]')
        dur = args.get('dur', '1')
        amp = args.get('amp', 0.7)
        oct_val = args.get('oct', 5)
        return f"{player} >> {synth}({notes}, dur={dur}, amp={amp}, oct={oct_val})"
    
    elif name == "play_drums":
        player = args.get('player', 'd1')
        pattern = args.get('pattern', 'x-o-')
        dur = args.get('dur', '0.5')
        amp = args.get('amp', 0.8)
        return f'{player} >> play("{pattern}", dur={dur}, amp={amp})'
    
    elif name == "set_tempo":
        return f"Clock.bpm = {args.get('bpm', 120)}"
    
    elif name == "set_scale":
        return f"Scale.default = Scale.{args.get('scale', 'major')}"
    
    elif name == "set_root":
        return f'Root.default = "{args.get("root", "C")}"'
    
    elif name == "stop_player":
        return f"{args.get('player', 'p1')}.stop()"
    
    elif name == "stop_all":
        return "Clock.clear()"
    
    return f"# Unknown function: {name}"


# ============================================================================
# SYSTEM PROMPT
# ============================================================================
SYSTEM_PROMPT = """You are an expert AI music producer using FoxDot for live coding.

Use the provided functions to create music. Available functions:
- play_synth: Create melodies, bass, chords, pads
- play_drums: Create drum patterns (x=kick, o=snare, -=hihat)
- set_tempo: Set BPM (house=120-130, techno=130-150, lofi=70-90)
- set_scale: Set scale (major, minor, dorian, pentatonic, blues)
- set_root: Set key (C, D, E, F, G, A, B)
- stop_player: Stop one player
- stop_all: Stop everything

Synths: pluck, bass, keys, piano, pads, blip, saw, charm, bell, soft
Players: p1-p9 (melody), d1-d9 (drums), b1-b4 (bass)

ALWAYS use functions to make changes. Be creative with patterns!"""


# ============================================================================
# STREAMING CHAT WITH SYNC GENERATOR (works with Streamlit)
# ============================================================================
def stream_chat_sync(user_message: str, thinking_container, response_container, tools_container):
    """Process message with real-time streaming using sync generator."""
    from google import genai
    from google.genai import types
    
    if not st.session_state.client:
        st.session_state.client = genai.Client(api_key=st.session_state.api_key)
    
    client = st.session_state.client
    model = st.session_state.selected_model
    
    # Add user message to contents
    st.session_state.contents.append(
        types.Content(role="user", parts=[types.Part(text=user_message)])
    )
    
    # Config with thinking and tools
    tools = types.Tool(function_declarations=FUNCTION_DECLARATIONS)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[tools],
        temperature=0.7,
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=-1
        )
    )
    
    full_thinking = ""
    full_response = ""
    function_calls = []
    accumulated_parts = []
    
    # Stream the response
    thinking_container.markdown("💭 *Thinking...*")
    
    stream = client.models.generate_content_stream(
        model=model,
        contents=st.session_state.contents,
        config=config
    )
    
    for chunk in stream:
        if not chunk.candidates:
            continue
            
        for part in chunk.candidates[0].content.parts:
            # Handle thinking
            if hasattr(part, 'thought') and part.thought and part.text:
                full_thinking += part.text
                thinking_container.markdown(f"""
                <div class="thinking-box">
                    <div style="font-size: 0.75rem; opacity: 0.7;">💭 Thinking</div>
                    {full_thinking[-1000:]}
                </div>
                """, unsafe_allow_html=True)
            
            # Handle function calls
            elif part.function_call:
                func_name = part.function_call.name
                func_args = dict(part.function_call.args)
                
                # Build and execute code
                code = build_code_from_function(func_name, func_args)
                
                tools_container.markdown(f"""
                <div class="tool-call-box">
                    <div class="tool-name">⚡ {func_name}</div>
                    <pre style="font-size: 0.8rem; color: #a0aec0;">{code}</pre>
                    <div style="color: #f6ad55;">⏳ Executing...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Execute if auto-execute is on
                if st.session_state.auto_execute:
                    result = execute_foxdot_code(code)
                    status = "✅ Playing!" if result.get('success') else f"❌ {result.get('error')}"
                else:
                    result = {"success": True, "code": code}
                    status = "📝 Code generated (auto-execute off)"
                
                function_calls.append({
                    "name": func_name,
                    "args": func_args,
                    "code": code,
                    "result": result,
                    "status": status
                })
                
                accumulated_parts.append(part)
                
                # Update display
                tools_container.markdown(f"""
                <div class="tool-call-box">
                    <div class="tool-name">⚡ {func_name}</div>
                    <pre style="font-size: 0.8rem; color: #a0aec0;">{code}</pre>
                    <div class="tool-result">{status}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Update music state
                update_music_state(func_name, func_args)
            
            # Handle text response
            elif part.text and not (hasattr(part, 'thought') and part.thought):
                full_response += part.text
                response_container.markdown(f"""
                <div class="assistant-message">
                    <div style="font-size: 0.7rem; opacity: 0.7;">🎹 FoxDot Agent</div>
                    {full_response}
                </div>
                """, unsafe_allow_html=True)
    
    # Handle function responses if there were function calls
    if function_calls:
        # Add model's function call response to contents
        st.session_state.contents.append(
            types.Content(role="model", parts=accumulated_parts)
        )
        
        # Add function responses
        response_parts = []
        for fc in function_calls:
            response_parts.append(
                types.Part.from_function_response(
                    name=fc["name"],
                    response={"status": fc["status"], "code": fc["code"]}
                )
            )
        st.session_state.contents.append(
            types.Content(role="user", parts=response_parts)
        )
        
        # Get final response after function calls
        final_stream = client.models.generate_content_stream(
            model=model,
            contents=st.session_state.contents,
            config=config
        )
        
        for chunk in final_stream:
            if not chunk.candidates:
                continue
            for part in chunk.candidates[0].content.parts:
                if part.text and not (hasattr(part, 'thought') and part.thought):
                    full_response += part.text
                    response_container.markdown(f"""
                    <div class="assistant-message">
                        <div style="font-size: 0.7rem; opacity: 0.7;">🎹 FoxDot Agent</div>
                        {full_response}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Add final model response to contents
        if full_response:
            st.session_state.contents.append(
                types.Content(role="model", parts=[types.Part(text=full_response)])
            )
    
    # Clear thinking if we got a response
    if full_response:
        thinking_container.empty()
    
    return {
        "response": full_response or "Done! Music is playing.",
        "thinking": full_thinking,
        "function_calls": function_calls
    }


def update_music_state(func_name: str, args: Dict):
    """Update music state based on function call."""
    if func_name == "set_tempo":
        st.session_state.music_state['bpm'] = args.get('bpm', 120)
    elif func_name == "set_scale":
        st.session_state.music_state['scale'] = args.get('scale', 'major')
    elif func_name == "set_root":
        st.session_state.music_state['root'] = args.get('root', 'C')
    elif func_name in ["play_synth", "play_drums"]:
        player = args.get('player', 'p1')
        synth = args.get('synth', 'play')
        st.session_state.music_state['layers'][player] = {'synth': synth, 'args': args}
    elif func_name == "stop_player":
        player = args.get('player')
        if player in st.session_state.music_state['layers']:
            del st.session_state.music_state['layers'][player]
    elif func_name == "stop_all":
        st.session_state.music_state['layers'] = {}


# ============================================================================
# UI COMPONENTS
# ============================================================================
def render_message(msg: Dict):
    """Render a chat message."""
    if msg['role'] == 'user':
        st.markdown(f"""
        <div class="user-message">
            <div style="font-size: 0.7rem; opacity: 0.7;">You</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div style="font-size: 0.7rem; opacity: 0.7;">🎹 FoxDot Agent</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
        
        if msg.get('function_calls'):
            with st.expander(f"🔧 Tool Calls ({len(msg['function_calls'])})"):
                for fc in msg['function_calls']:
                    st.code(fc.get('code', ''), language='python')
                    st.caption(fc.get('status', ''))
        
        if msg.get('thinking'):
            with st.expander("💭 Thinking"):
                st.text(msg['thinking'][:1000])


def render_sidebar():
    """Render sidebar."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        api_key = st.text_input("Google API Key", value=st.session_state.api_key, type="password")
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.session_state.client = None
        
        model = st.selectbox("Model", AVAILABLE_MODELS, 
                            index=AVAILABLE_MODELS.index(st.session_state.selected_model))
        st.session_state.selected_model = model
        
        auto_exec = st.toggle("Auto-execute code", value=st.session_state.auto_execute)
        st.session_state.auto_execute = auto_exec
        
        if auto_exec:
            st.warning("⚠️ **Required:** In SuperCollider, run: `FoxDot.start`")
        
        st.markdown("---")
        
        # Music state
        st.markdown("### 🎵 Music State")
        col1, col2, col3 = st.columns(3)
        col1.metric("BPM", st.session_state.music_state['bpm'])
        col2.metric("Scale", st.session_state.music_state['scale'])
        col3.metric("Root", st.session_state.music_state['root'])
        
        layers = st.session_state.music_state['layers']
        if layers:
            for name, layer in layers.items():
                st.markdown(f"""<div class="layer-item"><b>{name}</b> ({layer.get('synth', '?')})</div>""", 
                           unsafe_allow_html=True)
        else:
            st.info("No active layers")
        
        st.markdown("---")
        
        # Quick actions
        col1, col2 = st.columns(2)
        if col1.button("🛑 Stop All", use_container_width=True):
            stop_all_music()
            st.session_state.music_state['layers'] = {}
            st.rerun()
        
        if col2.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.contents = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Try These")
        for ex in ["Create a chill lo-fi beat at 80 BPM", "Make a techno track", "Add atmospheric pads"]:
            if st.button(ex, key=ex[:15]):
                st.session_state.pending = ex
                st.rerun()


# ============================================================================
# MAIN
# ============================================================================
def main():
    init_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="color: #4fd1c5;">🎹 FoxDot AI Music Agent</h1>
        <p style="color: #a0aec0;">Create music with AI • Real-time Streaming</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sidebar()
    
    # Check API key
    if not st.session_state.api_key:
        st.warning("⚠️ Enter your Google API key in the sidebar to get started")
        return
    
    # Display messages
    for msg in st.session_state.messages:
        render_message(msg)
    
    # Handle pending message from sidebar
    if 'pending' in st.session_state and st.session_state.pending:
        pending = st.session_state.pending
        st.session_state.pending = None
        process_input(pending)
    
    # Chat input
    if user_input := st.chat_input("Describe the music you want to create..."):
        process_input(user_input)


def process_input(user_input: str):
    """Process user input with streaming."""
    # Add user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    })
    
    # Create containers for streaming output
    thinking_container = st.empty()
    tools_container = st.empty()
    response_container = st.empty()
    
    # Run streaming
    try:
        result = stream_chat_sync(
            user_input,
            thinking_container,
            response_container,
            tools_container
        )
        
        # Save to messages
        st.session_state.messages.append({
            'role': 'assistant',
            'content': result.get('response', 'Done!'),
            'thinking': result.get('thinking', ''),
            'function_calls': result.get('function_calls', []),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    st.rerun()


if __name__ == "__main__":
    main()
