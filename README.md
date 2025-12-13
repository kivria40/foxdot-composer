# 🎹 FoxDot AI Music Agent

Create music with AI using natural language. Generate and live code music using Google Gemini and FoxDot, with real-time streaming, AI thinking visualization, and auto-execution in SuperCollider.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎨 Beautiful Streamlit UI
- **Real-time Streaming** - See AI responses stream in character by character
- **Thinking Visualization** - Watch the AI's reasoning process unfold
- **Tool Call Indicators** - Live function call execution with code preview
- **Music State Panel** - Live view of BPM, scale, root, and active layers

### 🤖 AI-Powered Music Creation
- **Natural Language Interface** - Describe music in plain English
- **Genre Understanding** - Knows house, techno, lo-fi, hip-hop, ambient, and more
- **Intelligent Layering** - AI maintains context of what's playing
- **Continuous Evolution** - Build and modify compositions layer by layer

### 🎵 FoxDot Integration
- **Global Environment** - Shared FoxDot state like the original working code
- **Auto-execution** - Code runs immediately in SuperCollider (default ON)
- **50+ Synths** - Full knowledge of FoxDot synthesizers
- **Effects & Scales** - Complete access to FoxDot's musical capabilities

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Set environment variable
export GOOGLE_API_KEY="your-api-key-here"

# Or enter it directly in the Streamlit UI
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Setup SuperCollider & FoxDot

**Install SuperCollider:**
- Download from [supercollider.github.io](https://supercollider.github.io/downloads)

**Start SuperCollider and run:**
```supercollider
FoxDot.start
```

**Wait for:** `FoxDot Quark ready!` message

### 4. Run the Streamlit UI

```bash
streamlit run src/ui/app.py
```

Or use the main.py launcher:
```bash
python main.py --ui
```

Open http://localhost:8501 and start creating music!

## 📁 Project Structure

```
foxdot-composer/
├── main.py                     # Entry point (CLI)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
└── src/
    ├── core/                   # Core logic
    │   ├── agent.py            # Main agent
    │   ├── streaming_agent.py  # Streaming support
    │   ├── session.py          # Session management
    │   ├── executor.py         # FoxDot execution
    │   ├── functions.py        # Gemini function declarations
    │   ├── prompts.py          # System prompts
    │   └── knowledge.py        # FoxDot knowledge base
    │
    └── ui/
        └── app.py              # Streamlit UI (main interface)
```

## 🎮 Usage Examples

### In the Streamlit UI

1. Enter your Google API key in the sidebar
2. Select your preferred model (gemini-2.5-flash recommended)
3. Enable auto-execute (default ON)
4. Type natural language requests:

```
"Create a chill lo-fi beat at 80 BPM"
→ Sets tempo, creates drums and melody

"Add a deep bass line"
→ Adds bass layer while keeping existing music

"Make it more atmospheric"
→ Adds reverb pads, adjusts layers

"Make the drums more complex"
→ Modifies drum pattern with fills
```

### Available Models
- **gemini-2.5-flash** - Fast, balanced (recommended)
- **gemini-2.5-flash-lite** - Faster, lighter
- **gemini-2.5-pro** - Most capable, slower

## 🎛️ Available Functions

The AI uses these functions to control music:

| Function | Description | Example |
|----------|-------------|---------|
| `play_synth` | Melodic layers (melody, bass, chords, pads) | `p1 >> pluck([0, 2, 4, 7])` |
| `play_drums` | Drum/percussion patterns | `d1 >> play("x-o-")` |
| `set_tempo` | Change BPM (40-200) | `Clock.bpm = 120` |
| `set_scale` | Musical scale | `Scale.default = Scale.minor` |
| `set_root` | Root note (C-B) | `Root.default = "C"` |
| `stop_player` | Stop specific layer | `p1.stop()` |
| `stop_all` | Stop everything | `Clock.clear()` |

### Synths Available
**Melody:** pluck, charm, bell, keys, soft, glass, star  
**Bass:** bass, sawbass, dub, jbass, fuzz, growl  
**Pads:** pads, sinepad, space, soft  
**Drums:** Use `play()` with pattern characters: `x`=kick, `o`=snare, `-`=hihat

## 🧠 How It Works

1. **Natural Language Input** - You describe music in plain English
2. **AI Thinking** - Gemini reasons about the request (visible in UI)
3. **Function Calling** - AI calls functions to build FoxDot code
4. **Code Generation** - FoxDot Python code is created
5. **Auto-execution** - Code runs in global FoxDot environment
6. **SuperCollider** - Audio is generated in real-time
7. **Streaming Response** - AI explains what it did

The UI updates in real-time showing thinking, tool calls, and responses as they stream in.

## 🎵 Genre Reference

| Genre | BPM | Key Elements |
|-------|-----|--------------|
| House | 120-130 | Four-on-floor kick, offbeat hats, chord stabs |
| Techno | 125-150 | Driving kick, minimal melody, filter sweeps |
| Lo-Fi | 70-90 | Relaxed feel, bitcrush, room reverb, swing |
| Ambient | 60-90 | Long sustains, heavy reverb, sparse drums |
| Drum & Bass | 160-180 | Breakbeats, heavy sub bass, fast hats |
| Hip-Hop | 85-115 | Boom bap drums, swing, piano/keys |

## ⚠️ Troubleshooting

**"SynthDef not found" errors:**
- Make sure you ran `FoxDot.start` in SuperCollider
- Wait for "FoxDot Quark ready!" message
- Restart SuperCollider if needed

**No sound:**
- Check SuperCollider is running
- Verify `FoxDot.start` was executed
- Check audio output settings in SuperCollider

**Streamlit errors:**
- Make sure you're in the `foxdot-composer/` directory
- Use: `streamlit run src/ui/app.py`

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional genre presets
- More function tools
- UI improvements
- Documentation

## 📄 License

MIT License

---

**Built with:** Google Gemini • FoxDot • SuperCollider • Streamlit

Co-authored-by: Claude (Anthropic)
