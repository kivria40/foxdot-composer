"""
FoxDot Session Manager - Maintains context, active layers, and chat history
Tracks all active players, their state, and enables continuous layering
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class PlayerState(Enum):
    """State of a player object."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


@dataclass
class Layer:
    """Represents a single music layer (player)."""
    player_name: str  # e.g., "p1", "d1", "b1"
    synth: str  # e.g., "pluck", "play", "bass"
    code: str  # The FoxDot code for this layer
    description: str  # Human description
    state: PlayerState = PlayerState.PLAYING
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    # Musical properties
    notes: Optional[List[int]] = None  # For melodic layers
    pattern: Optional[str] = None  # For drum/sample layers
    dur: Optional[Any] = None
    amp: Optional[float] = None
    oct: Optional[int] = None
    effects: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['state'] = self.state.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Layer':
        """Create from dictionary."""
        data['state'] = PlayerState(data.get('state', 'playing'))
        return cls(**data)


@dataclass 
class ChatMessage:
    """A single message in the conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    code_generated: Optional[str] = None  # FoxDot code if any was generated
    layers_affected: List[str] = field(default_factory=list)  # Which layers were modified
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MusicState:
    """Current state of the music composition."""
    bpm: int = 120
    scale: str = "major"
    root: str = "C"
    active_layers: Dict[str, Layer] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'bpm': self.bpm,
            'scale': self.scale,
            'root': self.root,
            'active_layers': {k: v.to_dict() for k, v in self.active_layers.items()}
        }


class FoxDotSession:
    """
    Manages a FoxDot live coding session with full context awareness.
    Tracks all layers, history, and provides context for the AI.
    """
    
    # Available player names
    MELODIC_PLAYERS = [f"p{i}" for i in range(1, 10)]  # p1-p9
    DRUM_PLAYERS = [f"d{i}" for i in range(1, 10)]  # d1-d9
    BASS_PLAYERS = [f"b{i}" for i in range(1, 5)]  # b1-b4
    PAD_PLAYERS = [f"pad{i}" for i in range(1, 4)]  # pad1-pad3
    
    def __init__(self, session_id: Optional[str] = None):
        """Initialize a new session."""
        self.session_id = session_id or datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.created_at = datetime.datetime.now().isoformat()
        
        # Music state
        self.music_state = MusicState()
        
        # Conversation history
        self.chat_history: List[ChatMessage] = []
        
        # Execution history (all code that was run)
        self.code_history: List[Dict[str, Any]] = []
        
        # Used players tracking
        self._used_players: Dict[str, bool] = {}
        
    def get_next_player(self, player_type: str = "melodic") -> str:
        """Get the next available player name."""
        if player_type == "drums" or player_type == "percussion":
            players = self.DRUM_PLAYERS
        elif player_type == "bass":
            players = self.BASS_PLAYERS
        elif player_type == "pad":
            players = self.PAD_PLAYERS
        else:
            players = self.MELODIC_PLAYERS
        
        for player in players:
            if player not in self.music_state.active_layers:
                return player
        
        # If all used, return first one (will replace)
        return players[0]
    
    def add_layer(
        self,
        player_name: str,
        synth: str,
        code: str,
        description: str,
        **musical_props
    ) -> Layer:
        """Add or update a layer."""
        layer = Layer(
            player_name=player_name,
            synth=synth,
            code=code,
            description=description,
            notes=musical_props.get('notes'),
            pattern=musical_props.get('pattern'),
            dur=musical_props.get('dur'),
            amp=musical_props.get('amp'),
            oct=musical_props.get('oct'),
            effects=musical_props.get('effects', {})
        )
        
        # If player exists, mark as modified
        if player_name in self.music_state.active_layers:
            layer.created_at = self.music_state.active_layers[player_name].created_at
        
        self.music_state.active_layers[player_name] = layer
        return layer
    
    def remove_layer(self, player_name: str) -> bool:
        """Remove a layer (stop player)."""
        if player_name in self.music_state.active_layers:
            self.music_state.active_layers[player_name].state = PlayerState.STOPPED
            del self.music_state.active_layers[player_name]
            return True
        return False
    
    def update_layer(self, player_name: str, **updates) -> Optional[Layer]:
        """Update specific properties of a layer."""
        if player_name not in self.music_state.active_layers:
            return None
        
        layer = self.music_state.active_layers[player_name]
        for key, value in updates.items():
            if hasattr(layer, key):
                setattr(layer, key, value)
        
        layer.modified_at = datetime.datetime.now().isoformat()
        return layer
    
    def get_layer(self, player_name: str) -> Optional[Layer]:
        """Get a specific layer."""
        return self.music_state.active_layers.get(player_name)
    
    def get_all_layers(self) -> Dict[str, Layer]:
        """Get all active layers."""
        return self.music_state.active_layers.copy()
    
    def set_tempo(self, bpm: int):
        """Set the tempo."""
        self.music_state.bpm = bpm
    
    def set_scale(self, scale: str):
        """Set the scale."""
        self.music_state.scale = scale
    
    def set_root(self, root: str):
        """Set the root note."""
        self.music_state.root = root
    
    def add_chat_message(
        self,
        role: str,
        content: str,
        code_generated: Optional[str] = None,
        layers_affected: Optional[List[str]] = None
    ) -> ChatMessage:
        """Add a message to chat history."""
        message = ChatMessage(
            role=role,
            content=content,
            code_generated=code_generated,
            layers_affected=layers_affected or []
        )
        self.chat_history.append(message)
        return message
    
    def add_code_execution(self, code: str, success: bool, output: str = ""):
        """Record a code execution."""
        self.code_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'code': code,
            'success': success,
            'output': output
        })
    
    def get_context_summary(self) -> str:
        """
        Generate a summary of current session state for AI context.
        This is what gets sent to the AI to maintain awareness.
        """
        summary_parts = [
            "## Current Music Session State\n"
        ]
        
        # Global settings
        summary_parts.append(f"**Tempo:** {self.music_state.bpm} BPM")
        summary_parts.append(f"**Scale:** {self.music_state.scale}")
        summary_parts.append(f"**Root:** {self.music_state.root}")
        summary_parts.append("")
        
        # Active layers
        if self.music_state.active_layers:
            summary_parts.append("### Active Layers (Currently Playing):")
            for name, layer in self.music_state.active_layers.items():
                layer_info = f"- **{name}** ({layer.synth}): {layer.description}"
                if layer.notes:
                    layer_info += f" | Notes: {layer.notes}"
                if layer.pattern:
                    layer_info += f" | Pattern: '{layer.pattern}'"
                if layer.amp:
                    layer_info += f" | Amp: {layer.amp}"
                summary_parts.append(layer_info)
        else:
            summary_parts.append("### No active layers - silence")
        
        summary_parts.append("")
        
        # Recent conversation (last 5 messages)
        if self.chat_history:
            summary_parts.append("### Recent Conversation:")
            recent = self.chat_history[-5:]
            for msg in recent:
                role_icon = "🎤" if msg.role == "user" else "🎹"
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                summary_parts.append(f"{role_icon} **{msg.role.title()}**: {content_preview}")
        
        return "\n".join(summary_parts)
    
    def get_full_context_for_ai(self) -> str:
        """
        Get complete context string for the AI, including:
        - Current state
        - Active code
        - Recent history
        """
        context_parts = [self.get_context_summary()]
        
        # Add all current code
        if self.music_state.active_layers:
            context_parts.append("\n### Current FoxDot Code Running:")
            context_parts.append("```python")
            context_parts.append(f"Clock.bpm = {self.music_state.bpm}")
            context_parts.append(f"Scale.default = Scale.{self.music_state.scale}")
            context_parts.append(f'Root.default = "{self.music_state.root}"')
            context_parts.append("")
            for name, layer in self.music_state.active_layers.items():
                context_parts.append(f"# {layer.description}")
                context_parts.append(layer.code)
                context_parts.append("")
            context_parts.append("```")
        
        return "\n".join(context_parts)
    
    def generate_full_code(self) -> str:
        """Generate complete FoxDot code for current state."""
        code_parts = [
            f"# FoxDot Session: {self.session_id}",
            f"# Generated: {datetime.datetime.now().isoformat()}",
            "",
            f"Clock.bpm = {self.music_state.bpm}",
            f"Scale.default = Scale.{self.music_state.scale}",
            f'Root.default = "{self.music_state.root}"',
            ""
        ]
        
        for name, layer in self.music_state.active_layers.items():
            code_parts.append(f"# {layer.description}")
            code_parts.append(layer.code)
            code_parts.append("")
        
        return "\n".join(code_parts)
    
    def clear_all(self):
        """Clear all layers (stop all music)."""
        self.music_state.active_layers.clear()
    
    def save_session(self, filepath: str):
        """Save session to a file."""
        data = {
            'session_id': self.session_id,
            'created_at': self.created_at,
            'music_state': self.music_state.to_dict(),
            'chat_history': [msg.to_dict() for msg in self.chat_history],
            'code_history': self.code_history
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_session(cls, filepath: str) -> 'FoxDotSession':
        """Load session from a file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        session = cls(session_id=data['session_id'])
        session.created_at = data['created_at']
        
        # Restore music state
        ms_data = data['music_state']
        session.music_state.bpm = ms_data['bpm']
        session.music_state.scale = ms_data['scale']
        session.music_state.root = ms_data['root']
        
        for name, layer_data in ms_data.get('active_layers', {}).items():
            session.music_state.active_layers[name] = Layer.from_dict(layer_data)
        
        # Restore chat history
        for msg_data in data.get('chat_history', []):
            session.chat_history.append(ChatMessage(**msg_data))
        
        session.code_history = data.get('code_history', [])
        
        return session
    
    def __repr__(self):
        return f"FoxDotSession(id={self.session_id}, layers={len(self.music_state.active_layers)}, messages={len(self.chat_history)})"


# Convenience functions for parsing AI-generated code

def parse_foxdot_code(code: str) -> Dict[str, Any]:
    """
    Parse FoxDot code to extract layers and settings.
    Returns structured information about what the code does.
    """
    import re
    
    result = {
        'bpm': None,
        'scale': None,
        'root': None,
        'players': {},
        'commands': []
    }
    
    lines = code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Check for Clock.bpm
        bpm_match = re.search(r'Clock\.bpm\s*=\s*(\d+)', line)
        if bpm_match:
            result['bpm'] = int(bpm_match.group(1))
            continue
        
        # Check for Scale.default
        scale_match = re.search(r'Scale\.default\s*=\s*Scale\.(\w+)', line)
        if scale_match:
            result['scale'] = scale_match.group(1)
            continue
        
        # Check for Root.default
        root_match = re.search(r'Root\.default\s*=\s*["\']?(\w+)["\']?', line)
        if root_match:
            result['root'] = root_match.group(1)
            continue
        
        # Check for player assignments (p1 >> synth(...))
        player_match = re.search(r'(\w+)\s*>>\s*(\w+)\s*\((.+)\)', line)
        if player_match:
            player_name = player_match.group(1)
            synth = player_match.group(2)
            args = player_match.group(3)
            
            result['players'][player_name] = {
                'synth': synth,
                'args': args,
                'full_code': line
            }
            continue
        
        # Check for Clock.clear()
        if 'Clock.clear()' in line:
            result['commands'].append('clear')
            continue
        
        # Check for .stop()
        stop_match = re.search(r'(\w+)\.stop\(\)', line)
        if stop_match:
            result['commands'].append(('stop', stop_match.group(1)))
    
    return result


def extract_layer_info(player_code: Dict) -> Dict[str, Any]:
    """Extract detailed info from a player's code."""
    import re
    
    args = player_code.get('args', '')
    
    info = {
        'synth': player_code.get('synth'),
        'notes': None,
        'pattern': None,
        'dur': None,
        'amp': None,
        'oct': None
    }
    
    # Check if it's a play() synth (samples)
    if info['synth'] == 'play':
        pattern_match = re.search(r'["\']([^"\']+)["\']', args)
        if pattern_match:
            info['pattern'] = pattern_match.group(1)
    else:
        # Extract notes array
        notes_match = re.search(r'\[([^\]]+)\]', args)
        if notes_match:
            try:
                notes_str = notes_match.group(1)
                info['notes'] = [int(n.strip()) for n in notes_str.split(',') if n.strip().lstrip('-').isdigit()]
            except:
                pass
    
    # Extract dur
    dur_match = re.search(r'dur\s*=\s*([^,\)]+)', args)
    if dur_match:
        info['dur'] = dur_match.group(1).strip()
    
    # Extract amp
    amp_match = re.search(r'amp\s*=\s*([\d.]+)', args)
    if amp_match:
        info['amp'] = float(amp_match.group(1))
    
    # Extract oct
    oct_match = re.search(r'oct\s*=\s*(\d+)', args)
    if oct_match:
        info['oct'] = int(oct_match.group(1))
    
    return info


if __name__ == "__main__":
    # Test the session manager
    session = FoxDotSession()
    
    # Add some test layers
    session.set_tempo(120)
    session.set_scale("minor")
    session.set_root("D")
    
    session.add_layer(
        "p1", "pluck",
        'p1 >> pluck([0, 2, 4, 7], dur=[1, 0.5, 0.5], amp=0.7)',
        "Melodic arpeggio pattern",
        notes=[0, 2, 4, 7],
        dur=[1, 0.5, 0.5],
        amp=0.7
    )
    
    session.add_layer(
        "d1", "play",
        'd1 >> play("x-o-x-o-", amp=0.9)',
        "Basic house beat",
        pattern="x-o-x-o-",
        amp=0.9
    )
    
    session.add_chat_message("user", "Create a chill lo-fi beat")
    session.add_chat_message("assistant", "Here's a relaxed lo-fi beat with soft drums and keys", 
                            code_generated="p1 >> keys([0,2,4], dur=1)")
    
    print(session)
    print("\n" + "="*50)
    print(session.get_context_summary())
    print("\n" + "="*50)
    print(session.generate_full_code())
