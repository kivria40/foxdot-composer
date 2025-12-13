"""
FoxDot Function Declarations and Executors
All Gemini function calling definitions for music control
"""

from typing import Dict, Any, Optional, List

# =============================================================================
# FUNCTION DECLARATIONS
# =============================================================================

PLAY_SYNTH_FUNCTION = {
    "name": "play_synth",
    "description": """Play a melodic synthesizer with specified notes and parameters.
    Use this to create melodies, basslines, chord progressions, and lead lines.
    The synth will play on a specific player (p1-p9, b1-b4, etc.).""",
    "parameters": {
        "type": "object",
        "properties": {
            "player": {
                "type": "string",
                "description": "Player name (p1-p9 for melody, b1-b4 for bass, pad1-pad3 for pads)",
                "enum": ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", 
                         "b1", "b2", "b3", "b4", "pad1", "pad2", "pad3"]
            },
            "synth": {
                "type": "string",
                "description": "Synth name (pluck, bass, keys, piano, pads, blip, saw, etc.)"
            },
            "notes": {
                "type": "string",
                "description": "Notes pattern as Python list string, e.g., '[0, 2, 4, 7]' or '[(0,2,4), 1, 2]' for chords"
            },
            "dur": {
                "type": "string",
                "description": "Duration pattern, e.g., '1', '[1, 0.5, 0.5]', '1/4'"
            },
            "amp": {
                "type": "number",
                "description": "Amplitude/volume (0.0 to 1.0)"
            },
            "oct": {
                "type": "integer",
                "description": "Octave (3-7, default 5)"
            },
            "description": {
                "type": "string",
                "description": "Human-readable description of this layer"
            },
            "effects": {
                "type": "object",
                "description": "Optional effects like room, lpf, vib, slide, etc.",
                "properties": {
                    "room": {"type": "number", "description": "Reverb amount (0-1)"},
                    "lpf": {"type": "integer", "description": "Low-pass filter frequency"},
                    "hpf": {"type": "integer", "description": "High-pass filter frequency"},
                    "vib": {"type": "number", "description": "Vibrato depth"},
                    "slide": {"type": "number", "description": "Pitch slide amount"},
                    "chop": {"type": "integer", "description": "Chop into pieces"},
                    "pan": {"type": "number", "description": "Stereo pan (-1 to 1)"}
                }
            }
        },
        "required": ["player", "synth", "notes", "description"]
    }
}

PLAY_DRUMS_FUNCTION = {
    "name": "play_drums",
    "description": """Play a drum/percussion pattern using sample characters.
    Use 'x' for kick, 'o' for snare, '-' for hi-hat, '*' for clap, etc.
    Special brackets: [] for subdivision, () for alternation, {} for random.""",
    "parameters": {
        "type": "object",
        "properties": {
            "player": {
                "type": "string",
                "description": "Drum player name (d1-d9)",
                "enum": ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9"]
            },
            "pattern": {
                "type": "string",
                "description": "Drum pattern string, e.g., 'x-o-x-o-' or 'x--o--x-o-'"
            },
            "dur": {
                "type": "string",
                "description": "Duration pattern, e.g., '1', '0.5', '[1, 0.5]'"
            },
            "amp": {
                "type": "number",
                "description": "Amplitude/volume (0.0 to 1.0)"
            },
            "description": {
                "type": "string",
                "description": "Human-readable description of this drum pattern"
            },
            "effects": {
                "type": "object",
                "description": "Optional effects",
                "properties": {
                    "room": {"type": "number"},
                    "sample": {"type": "integer", "description": "Sample variation number"},
                    "rate": {"type": "number", "description": "Playback rate"},
                    "pan": {"type": "number"},
                    "lpf": {"type": "integer"},
                    "coarse": {"type": "integer", "description": "Bit crush amount"}
                }
            }
        },
        "required": ["player", "pattern", "description"]
    }
}

SET_TEMPO_FUNCTION = {
    "name": "set_tempo",
    "description": "Set the tempo in beats per minute (BPM). Typical ranges: ambient 60-90, hip-hop 85-115, house 120-130, techno 125-150, drum & bass 160-180.",
    "parameters": {
        "type": "object",
        "properties": {
            "bpm": {
                "type": "integer",
                "description": "Tempo in beats per minute (40-200)"
            }
        },
        "required": ["bpm"]
    }
}

SET_SCALE_FUNCTION = {
    "name": "set_scale",
    "description": "Set the musical scale for all players. Available: major, minor, dorian, phrygian, lydian, mixolydian, pentatonic, blues, etc.",
    "parameters": {
        "type": "object",
        "properties": {
            "scale": {
                "type": "string",
                "description": "Scale name",
                "enum": ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian", 
                         "locrian", "pentatonic", "minorPentatonic", "blues", "harmonicMinor",
                         "melodicMinor", "whole", "chromatic", "egyptian", "japanese", "chinese"]
            }
        },
        "required": ["scale"]
    }
}

SET_ROOT_FUNCTION = {
    "name": "set_root",
    "description": "Set the root note (key) for all players.",
    "parameters": {
        "type": "object",
        "properties": {
            "root": {
                "type": "string",
                "description": "Root note name",
                "enum": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
                         "Db", "Eb", "Gb", "Ab", "Bb"]
            }
        },
        "required": ["root"]
    }
}

STOP_PLAYER_FUNCTION = {
    "name": "stop_player",
    "description": "Stop a specific player from playing.",
    "parameters": {
        "type": "object",
        "properties": {
            "player": {
                "type": "string",
                "description": "Player name to stop (p1-p9, d1-d9, b1-b4, etc.)"
            }
        },
        "required": ["player"]
    }
}

STOP_ALL_FUNCTION = {
    "name": "stop_all",
    "description": "Stop all music and clear all players. Use when user wants silence or to start fresh.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

MODIFY_LAYER_FUNCTION = {
    "name": "modify_layer",
    "description": "Modify an existing layer's parameters without changing its core pattern.",
    "parameters": {
        "type": "object",
        "properties": {
            "player": {
                "type": "string",
                "description": "Player name to modify"
            },
            "amp": {
                "type": "number",
                "description": "New amplitude"
            },
            "oct": {
                "type": "integer",
                "description": "New octave"
            },
            "effects": {
                "type": "object",
                "description": "Effects to add/change",
                "properties": {
                    "room": {"type": "number"},
                    "lpf": {"type": "integer"},
                    "hpf": {"type": "integer"},
                    "vib": {"type": "number"},
                    "pan": {"type": "number"},
                    "chop": {"type": "integer"}
                }
            }
        },
        "required": ["player"]
    }
}

EXECUTE_CODE_FUNCTION = {
    "name": "execute_code",
    "description": "Execute raw FoxDot code directly. Use for advanced patterns or features not covered by other functions.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Raw FoxDot Python code to execute"
            },
            "description": {
                "type": "string",
                "description": "Description of what the code does"
            }
        },
        "required": ["code", "description"]
    }
}

GET_SESSION_STATE_FUNCTION = {
    "name": "get_session_state",
    "description": "Get the current state of the music session including all active layers, tempo, scale, etc.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

# All function declarations for export
ALL_FUNCTION_DECLARATIONS = [
    PLAY_SYNTH_FUNCTION,
    PLAY_DRUMS_FUNCTION,
    SET_TEMPO_FUNCTION,
    SET_SCALE_FUNCTION,
    SET_ROOT_FUNCTION,
    STOP_PLAYER_FUNCTION,
    STOP_ALL_FUNCTION,
    MODIFY_LAYER_FUNCTION,
    EXECUTE_CODE_FUNCTION,
    GET_SESSION_STATE_FUNCTION,
]


# =============================================================================
# CODE BUILDERS
# =============================================================================

def build_foxdot_code(func_name: str, args: Dict[str, Any], session) -> Optional[str]:
    """Build FoxDot code from a function call."""
    
    if func_name == "play_synth":
        player = args['player']
        synth = args['synth']
        notes = args['notes']
        dur = args.get('dur', '1')
        amp = args.get('amp', 0.7)
        oct_val = args.get('oct', 5)
        effects = args.get('effects', {})
        
        params = [notes]
        params.append(f"dur={dur}")
        params.append(f"amp={amp}")
        params.append(f"oct={oct_val}")
        
        for effect, value in effects.items():
            params.append(f"{effect}={value}")
        
        return f"{player} >> {synth}({', '.join(params)})"
    
    elif func_name == "play_drums":
        player = args['player']
        pattern = args['pattern']
        dur = args.get('dur', '0.5')
        amp = args.get('amp', 0.8)
        effects = args.get('effects', {})
        
        params = [f'"{pattern}"']
        params.append(f"dur={dur}")
        params.append(f"amp={amp}")
        
        for effect, value in effects.items():
            params.append(f"{effect}={value}")
        
        return f'{player} >> play({", ".join(params)})'
    
    elif func_name == "set_tempo":
        return f"Clock.bpm = {args['bpm']}"
    
    elif func_name == "set_scale":
        return f"Scale.default = Scale.{args['scale']}"
    
    elif func_name == "set_root":
        return f'Root.default = "{args["root"]}"'
    
    elif func_name == "stop_player":
        return f"{args['player']}.stop()"
    
    elif func_name == "stop_all":
        return "Clock.clear()"
    
    elif func_name == "modify_layer":
        player = args['player']
        layer = session.get_layer(player)
        if not layer:
            return f"# Error: Player {player} not found"
        
        new_amp = args.get('amp', layer.amp)
        new_oct = args.get('oct', layer.oct)
        new_effects = {**layer.effects, **args.get('effects', {})}
        
        if layer.synth == 'play':
            params = [f'"{layer.pattern}"']
        else:
            params = [str(layer.notes)]
        
        if layer.dur:
            params.append(f"dur={layer.dur}")
        if new_amp:
            params.append(f"amp={new_amp}")
        if new_oct:
            params.append(f"oct={new_oct}")
        
        for effect, value in new_effects.items():
            params.append(f"{effect}={value}")
        
        return f"{player} >> {layer.synth}({', '.join(params)})"
    
    elif func_name == "execute_code":
        return args['code']
    
    elif func_name == "get_session_state":
        return None
    
    return f"# Unknown function: {func_name}"


def execute_function(
    func_name: str, 
    args: Dict[str, Any], 
    session, 
    executor,
    auto_execute: bool = True
) -> Dict[str, Any]:
    """Execute a function and return the result."""
    
    # Handle get_session_state specially
    if func_name == "get_session_state":
        return {
            "status": "success",
            "state": session.get_context_summary()
        }
    
    # Build the code
    code = build_foxdot_code(func_name, args, session)
    if not code:
        return {"status": "error", "message": "Could not build code for function"}
    
    # Update session state
    if func_name == "set_tempo":
        session.set_tempo(args['bpm'])
    elif func_name == "set_scale":
        session.set_scale(args['scale'])
    elif func_name == "set_root":
        session.set_root(args['root'])
    elif func_name == "stop_all":
        session.clear_all()
    elif func_name == "stop_player":
        session.remove_layer(args['player'])
    elif func_name in ["play_synth", "play_drums"]:
        player = args['player']
        synth = args.get('synth', 'play')
        desc = args.get('description', 'Layer')
        
        session.add_layer(
            player_name=player,
            synth=synth,
            code=code,
            description=desc,
            notes=eval(args['notes']) if 'notes' in args else None,
            pattern=args.get('pattern'),
            dur=args.get('dur'),
            amp=args.get('amp'),
            oct=args.get('oct'),
            effects=args.get('effects', {})
        )
    
    # Execute if enabled
    if auto_execute:
        result = executor.execute(code, args.get('description'))
        session.add_code_execution(code, result.success, result.output)
        
        return {
            "status": "success" if result.success else "error",
            "code": code,
            "output": result.output,
            "error": result.error,
            "players_affected": result.players_affected
        }
    else:
        return {
            "status": "code_generated",
            "code": code,
            "message": "Code generated but not executed"
        }


# Helper to get function info by name
def get_function_info(name: str) -> Optional[Dict]:
    """Get function declaration by name."""
    for func in ALL_FUNCTION_DECLARATIONS:
        if func["name"] == name:
            return func
    return None
