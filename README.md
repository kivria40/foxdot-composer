# 🎹 FoxDot AI Music Agent

An AI-powered live coding music agent that uses Google Gemini 2.5 with function calling to create, modify, and evolve music in real-time using FoxDot and SuperCollider.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🤖 AI-Powered Music Creation
- **Natural Language Interface** - Describe music in plain English
- **Intelligent Layering** - AI maintains context of what's playing
- **Genre Understanding** - Knows house, techno, lo-fi, ambient, and more
- **Continuous Evolution** - Build and modify compositions layer by layer

### 🎨 Beautiful Streamlit UI
- **Streaming Responses** - See AI responses in real-time
- **Thinking Indicator** - Watch the AI reason about your request
- **Tool Call Visualization** - See function calls as they happen
- **Music State Panel** - Live view of tempo, scale, and layers

### 🧠 Smart Context Management
- **Full Conversation History** - AI remembers the entire session
- **Context Consolidation** - Automatic summarization when context gets large
- **Session Persistence** - Save and load your compositions

### 🎵 FoxDot Integration
- **50+ Synths** - Full knowledge of FoxDot synthesizers
- **Sample Library** - All drum samples and characters
- **Effects Chain** - Reverb, filters, delay, and more
- **Scales & Modes** - Major, minor, pentatonic, blues, and exotic scales

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd music
pip install -r requirements.txt
```

### 2. Set API Key

```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY = "your-api-key-here"

# Or create a .env file
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Run the Agent

**Option A: Beautiful Web UI (Recommended)**
```bash
python main.py --ui
```

**Option B: Terminal Interface**
```bash
python main.py
```

**Option C: Demo Mode (No FoxDot Required)**
```bash
python main.py --demo
```

## 📁 Project Structure

```
music/
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
├── README.md                   # This file
│
├── src/
│   ├── core/                   # Core agent logic
│   │   ├── agent.py            # Main FoxDot Agent
│   │   ├── streaming_agent.py  # Streaming with thinking support
│   │   ├── session.py          # Session & context management
│   │   ├── executor.py         # FoxDot code execution
│   │   ├── functions.py        # Gemini function declarations
│   │   ├── prompts.py          # System prompts
│   │   └── knowledge.py        # FoxDot knowledge base
│   │
│   └── ui/
│       └── app.py              # Streamlit web interface
│
└── sessions/                   # Saved sessions (auto-created)
```

## 🎮 Usage Examples

### Creating Music
```
You: Create a chill lo-fi beat at 80 BPM
Agent: *Sets tempo to 80, creates mellow drums and keys*

You: Add a deep bass line
Agent: *Adds bass layer, maintains drums and keys*

You: Make it more atmospheric
Agent: *Adds reverb pads, adjusts existing layers*
```

### Modifying Music
```
You: Make the drums more complex
You: Add some swing to the beat
You: Put a filter sweep on the bass
You: Stop the hi-hats
```

### Commands
- `stop` - Stop all music immediately
- `code` - Show current FoxDot code
- `state` - Show music state (tempo, scale, layers)
- `save <name>` - Save session to file
- `quit` - Exit the agent

## 🎛️ Available Functions

The AI can use these tools to control music:

| Function | Description |
|----------|-------------|
| `play_synth` | Create melodic layers (melody, bass, chords, pads) |
| `play_drums` | Create drum/percussion patterns |
| `set_tempo` | Change BPM (40-200) |
| `set_scale` | Set musical scale (major, minor, pentatonic, etc.) |
| `set_root` | Set key/root note (C, D, E, etc.) |
| `stop_player` | Stop a specific layer |
| `stop_all` | Stop all music |
| `modify_layer` | Adjust existing layer parameters |
| `execute_code` | Run raw FoxDot code |
| `get_session_state` | Check current music state |

## 🎹 FoxDot Setup (Optional)

For actual audio output, you need:

1. **SuperCollider** - Download from [supercollider.github.io](https://supercollider.github.io/downloads)

2. **FoxDot** - Install with pip:
   ```bash
   pip install FoxDot
   ```

3. **Start SuperCollider** - Open SuperCollider and run:
   ```supercollider
   FoxDot.start
   ```

4. **Run Agent in Live Mode**:
   ```bash
   python main.py  # Without --demo flag
   ```

## 🧠 Thinking & Streaming

The agent uses Gemini 2.5's thinking feature to:
- Break down complex musical requests
- Plan layer arrangements
- Reason about genre conventions
- Consider existing context

In the UI, you can expand the "💭 AI Thinking Process" section to see this reasoning.

## 📊 Context Consolidation

When conversation history gets large, the agent automatically:
1. Summarizes older conversation turns
2. Preserves key musical decisions
3. Keeps recent turns verbatim
4. Maintains awareness of current state

This ensures the AI stays responsive even in long sessions.

## 🎵 Genre Reference

| Genre | BPM | Key Elements |
|-------|-----|--------------|
| House | 120-130 | Four-on-floor kick, offbeat hats |
| Techno | 125-150 | Driving kick, minimal melody |
| Lo-Fi | 70-90 | Relaxed, bitcrush, room reverb |
| Ambient | 60-90 | Long sustains, heavy reverb |
| Drum & Bass | 160-180 | Breakbeats, heavy sub bass |
| Hip-Hop | 85-115 | Boom bap drums, swing feel |

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional synth presets
- Genre-specific patterns
- UI improvements
- Multi-model support

## 📄 License

MIT License - see LICENSE file for details.

---

Made with 🎵 by AI + Human collaboration
