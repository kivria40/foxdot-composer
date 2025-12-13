"""
AI Music Agent using Google GenAI SDK (Gemini 2.5) and FoxDot
This agent takes natural language prompts and generates live coded music using FoxDot.
"""

import os
import re
from google import genai
from google.genai import types

# Initialize the Gemini client
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# FoxDot globals (will be populated when initialized)
foxdot_env = {}

# System prompt for the music agent
SYSTEM_PROMPT = """You are an expert AI music producer and live coder specializing in FoxDot, 
a Python library for live coding music and algorithmic composition.

Your role is to:
1. Understand music requests from users (genres, moods, tempo, instruments, patterns)
2. Generate valid FoxDot Python code that creates the requested music
3. Explain what the code does musically

FoxDot Basics you must use:
- Players: p1, p2, p3, etc. (up to p9) - these play sounds
- Synths: pluck, bass, piano, blip, saw, sinepad, charm, bell, soprano, etc.
- Samples: play, loop - for drum patterns
- Patterns: P[0,1,2,3], PRange(8), PRand([0,1,2]), etc.
- Attributes: dur (duration), amp (amplitude), pan, oct (octave), scale, root
- Scales: Scale.major, Scale.minor, Scale.dorian, Scale.pentatonic, etc.
- Effects: room (reverb), spin, chop, slide, bend, etc.

Example FoxDot code:
```python
# Set tempo
Clock.bpm = 120

# Set scale
Scale.default = Scale.minor
Root.default = "C"

# Bass line
b1 >> bass([0, 2, 3, 5], dur=1, amp=0.8)

# Melody
p1 >> pluck(P[0, 2, 4, 7, 5, 3], dur=[0.5, 0.5, 1], oct=5)

# Drums
d1 >> play("x-o-", amp=0.9)

# Hihat
d2 >> play("--[--]", amp=0.5)
```

IMPORTANT RULES:
1. Always output ONLY valid FoxDot Python code
2. Use comments to explain what each part does
3. Start with Clock.bpm to set tempo
4. Use Scale.default and Root.default for key/scale
5. Limit to 4-6 players for clarity
6. Use realistic amp values (0.3-1.0)
7. To stop all: use Clock.clear()

When asked to stop or silence music, output: Clock.clear()

Output ONLY the FoxDot code block, no other text.
"""


class MusicAgent:
    """AI Agent that generates and plays FoxDot music based on natural language prompts."""
    
    def __init__(self, model_name: str = "gemini-flash-latest"):
        """
        Initialize the Music Agent.
        
        Args:
            model_name: The Gemini model to use (default: gemini-flash-latest)
        """
        self.model_name = model_name
        self.chat_history = []
        self.foxdot_initialized = False
        
    def initialize_foxdot(self):
        """Initialize FoxDot for live coding."""
        global foxdot_env
        if not self.foxdot_initialized:
            try:
                # Import FoxDot components into global namespace
                import FoxDot
                from FoxDot import Clock, Scale, Root
                
                # Get all FoxDot exports
                foxdot_env = {name: getattr(FoxDot, name) for name in dir(FoxDot) if not name.startswith('_')}
                foxdot_env['Clock'] = Clock
                foxdot_env['Scale'] = Scale
                foxdot_env['Root'] = Root
                
                self.foxdot_initialized = True
                print("✓ FoxDot initialized successfully!")
                print("✓ SuperCollider connection established.")
                return True
            except ImportError:
                print("✗ Error: FoxDot not installed. Install with: pip install FoxDot")
                return False
            except Exception as e:
                print(f"✗ Error initializing FoxDot: {e}")
                print("  Make sure SuperCollider is running with FoxDot.start")
                return False
        return True
    
    def extract_code(self, response_text: str) -> str:
        """Extract Python code from the response."""
        # Try to find code blocks
        code_pattern = r'```(?:python)?\n?(.*?)```'
        matches = re.findall(code_pattern, response_text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, return the whole response (might be raw code)
        return response_text.strip()
    
    def generate_music_code(self, prompt: str) -> str:
        """
        Generate FoxDot code based on user's music request.
        
        Args:
            prompt: Natural language description of desired music
            
        Returns:
            Generated FoxDot Python code
        """
        try:
            # Create the full prompt
            full_prompt = f"User request: {prompt}\n\nGenerate FoxDot code:"
            
            # Generate response using Gemini
            response = client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            
            # Extract and return the code
            code = self.extract_code(response.text)
            return code
            
        except Exception as e:
            return f"# Error generating music: {e}"
    
    def play_music(self, code: str) -> bool:
        """
        Execute FoxDot code to play music.
        
        Args:
            code: FoxDot Python code to execute
            
        Returns:
            True if successful, False otherwise
        """
        if not self.initialize_foxdot():
            return False
        
        try:
            # Execute the FoxDot code with FoxDot environment
            exec(code, foxdot_env)
            return True
        except Exception as e:
            print(f"✗ Error executing music code: {e}")
            return False
    
    def stop_music(self):
        """Stop all currently playing music."""
        try:
            if foxdot_env and 'Clock' in foxdot_env:
                foxdot_env['Clock'].clear()
                print("♪ Music stopped.")
            else:
                print("FoxDot not initialized yet.")
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def process_request(self, user_input: str) -> dict:
        """
        Process a user's music request end-to-end.
        
        Args:
            user_input: Natural language music request
            
        Returns:
            Dictionary with 'code' and 'success' keys
        """
        # Check for stop commands
        stop_keywords = ['stop', 'silence', 'quiet', 'halt', 'end', 'clear']
        if any(keyword in user_input.lower() for keyword in stop_keywords):
            self.stop_music()
            return {'code': 'Clock.clear()', 'success': True}
        
        # Generate the music code
        print(f"\n🎵 Generating music for: {user_input}")
        code = self.generate_music_code(user_input)
        
        print("\n📝 Generated FoxDot Code:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        
        # Play the music
        print("\n▶ Playing music...")
        success = self.play_music(code)
        
        if success:
            print("✓ Music is now playing!")
        
        return {'code': code, 'success': success}


def interactive_session():
    """Run an interactive music generation session."""
    print("=" * 50)
    print("🎹 AI Music Agent - FoxDot Live Coder")
    print("=" * 50)
    print("\nPowered by Google Gemini 2.5 and FoxDot")
    print("\nDescribe the music you want to create!")
    print("Examples:")
    print("  - 'Create a chill lo-fi beat with soft piano'")
    print("  - 'Make an energetic techno track at 140 BPM'")
    print("  - 'Play a jazzy melody in C minor'")
    print("  - 'Stop the music'")
    print("\nType 'quit' or 'exit' to end the session.")
    print("=" * 50)
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠ Warning: GOOGLE_API_KEY environment variable not set!")
        print("Set it with: $env:GOOGLE_API_KEY = 'your-api-key'")
        return
    
    agent = MusicAgent()
    
    while True:
        try:
            user_input = input("\n🎤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                agent.stop_music()
                print("\n👋 Thanks for making music! Goodbye!")
                break
            
            agent.process_request(user_input)
            
        except KeyboardInterrupt:
            agent.stop_music()
            print("\n\n👋 Session interrupted. Goodbye!")
            break


def demo_mode():
    """Run a demo without FoxDot (just generates code)."""
    print("=" * 50)
    print("🎹 AI Music Agent - DEMO MODE")
    print("=" * 50)
    print("\n(Demo mode - generates code without playing)")
    
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠ Set GOOGLE_API_KEY to use the AI agent")
        print("Example: $env:GOOGLE_API_KEY = 'your-api-key'")
        return
    
    agent = MusicAgent()
    
    demo_prompts = [
        "Create a relaxing ambient soundscape with slow pads",
        "Make a funky bass line with drums",
        "Play a simple melody in pentatonic scale"
    ]
    
    for prompt in demo_prompts:
        print(f"\n📝 Prompt: {prompt}")
        code = agent.generate_music_code(prompt)
        print(f"\n🎵 Generated Code:\n{code}\n")
        print("-" * 40)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_session()
