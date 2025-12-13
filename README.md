# 🎹 AI Music Agent - FoxDot Live Coder

An AI-powered music agent that uses **Google Gemini 2.5** to generate and play live-coded music using **FoxDot**.

## Features

- 🎵 Natural language to music generation
- 🤖 Powered by Google Gemini 2.5 (latest GenAI SDK)
- 🎹 Live coding with FoxDot
- 🔊 Real-time music playback via SuperCollider
- 💬 Interactive chat interface

## Prerequisites

1. **Python 3.8+**
2. **SuperCollider** - Download from [supercollider.github.io](https://supercollider.github.io/downloads)
3. **Google API Key** - Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install google-genai FoxDot
```

### 2. Install SuperCollider

Download and install SuperCollider from the official website. This is required for FoxDot to produce sound.

### 3. Setup FoxDot with SuperCollider

Open SuperCollider and run:
```supercollider
Quarks.install("FoxDot")
```

Then recompile the class library (Ctrl+Shift+L or Cmd+Shift+L on Mac).

### 4. Set your Google API Key

**Windows PowerShell:**
```powershell
$env:GOOGLE_API_KEY = "your-api-key-here"
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

### Start SuperCollider First

Before running the agent, start SuperCollider and run:
```supercollider
FoxDot.start
```

### Run the Agent

**Interactive Mode:**
```bash
python music_agent.py
```

**Demo Mode (generates code without playing):**
```bash
python music_agent.py --demo
```

### Example Prompts

- "Create a chill lo-fi beat with soft piano"
- "Make an energetic techno track at 140 BPM"
- "Play a jazzy melody in C minor"
- "Create ambient pads with reverb"
- "Make a funky bass line with drums"
- "Stop the music"

## How It Works

1. **User Input**: You describe the music you want in natural language
2. **AI Generation**: Gemini 2.5 generates valid FoxDot Python code
3. **Live Execution**: FoxDot executes the code in real-time
4. **Sound Output**: SuperCollider synthesizes and plays the audio

## Project Structure

```
music/
├── music_agent.py      # Main AI agent code
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### "FoxDot not installed"
```bash
pip install FoxDot
```

### "SuperCollider connection failed"
Make sure SuperCollider is running and you've executed `FoxDot.start` in it.

### "GOOGLE_API_KEY not set"
Set the environment variable with your API key (see Installation step 4).

### No sound output
Check that:
1. SuperCollider is running
2. `FoxDot.start` was executed in SuperCollider
3. Your system audio is working

## License

MIT License
