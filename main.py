"""
FoxDot Music Agent - CLI Entry Point
Interactive terminal interface
"""

import os
import sys
import json
import argparse

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def interactive_session(demo_mode: bool = False):
    """Run an interactive FoxDot music session."""
    from src.core.agent import FoxDotAgent
    
    print("=" * 60)
    print("🎹 FoxDot AI Music Agent")
    print("=" * 60)
    print("\nPowered by Google Gemini with Function Calling")
    print("\nDescribe the music you want to create!")
    print("The AI will build layers and maintain full context.")
    print("\nExamples:")
    print("  - 'Create a chill lo-fi beat at 80 BPM'")
    print("  - 'Add a soft piano melody in C minor'")
    print("  - 'Make the drums more complex'")
    print("  - 'Add reverb to everything'")
    print("  - 'Stop the bass'")
    print("  - 'Show me what's playing'")
    print("\nCommands:")
    print("  'quit' / 'exit' - End session")
    print("  'stop' - Stop all music")
    print("  'code' - Show current FoxDot code")
    print("  'save <filename>' - Save session")
    print("  'state' - Show current music state")
    print("=" * 60)
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠ GOOGLE_API_KEY not set!")
        print("Set with: $env:GOOGLE_API_KEY = 'your-api-key'")
        return
    
    try:
        agent = FoxDotAgent(auto_execute=not demo_mode)
        mode_str = "DEMO MODE" if demo_mode else "LIVE MODE"
        print(f"\n✓ Agent initialized! ({mode_str})")
        if not demo_mode:
            print("✓ Make sure SuperCollider is running with FoxDot.start")
        print()
        
    except Exception as e:
        print(f"\n✗ Error initializing agent: {e}")
        return
    
    while True:
        try:
            user_input = input("\n🎤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                agent.stop_all_music()
                print("\n👋 Thanks for making music! Goodbye!")
                break
            
            if user_input.lower() == 'stop':
                agent.stop_all_music()
                print("🔇 All music stopped.")
                continue
            
            if user_input.lower() == 'code':
                print("\n📝 Current FoxDot Code:")
                print("-" * 40)
                print(agent.get_current_code())
                print("-" * 40)
                continue
            
            if user_input.lower() == 'state':
                state = agent.get_session_state()
                print("\n🎵 Music State:")
                print(json.dumps(state, indent=2))
                continue
            
            if user_input.lower().startswith('save '):
                filename = user_input[5:].strip()
                if not filename.endswith('.json'):
                    filename += '.json'
                agent.save_session(filename)
                print(f"💾 Session saved to {filename}")
                continue
            
            # Process with AI
            print("\n🎹 Processing...")
            result = agent.chat(user_input)
            
            # Display thinking if present
            if result.get('thinking'):
                print(f"\n💭 Thoughts: {result['thinking'][:200]}...")
            
            print(f"\n🎹 Agent: {result['response']}")
            
            # Show function calls
            if result.get('function_calls'):
                print("\n📞 Functions called:")
                for fc in result['function_calls']:
                    status = fc.get('result', {}).get('status', 'unknown')
                    print(f"  ✓ {fc['name']} - {status}")
                    if fc.get('result', {}).get('code'):
                        print(f"    Code: {fc['result']['code']}")
        
        except KeyboardInterrupt:
            agent.stop_all_music()
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            continue


def run_streamlit():
    """Launch the Streamlit UI."""
    import subprocess
    app_path = os.path.join(os.path.dirname(__file__), 'src', 'ui', 'app.py')
    subprocess.run(['streamlit', 'run', app_path])


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="FoxDot AI Music Agent")
    parser.add_argument('--ui', action='store_true', help='Launch Streamlit UI')
    parser.add_argument('--demo', action='store_true', help='Demo mode (no FoxDot execution)')
    parser.add_argument('--api-key', type=str, help='Google API key')
    
    args = parser.parse_args()
    
    # Set API key if provided
    if args.api_key:
        os.environ['GOOGLE_API_KEY'] = args.api_key
    
    if args.ui:
        run_streamlit()
    else:
        interactive_session(demo_mode=args.demo)


if __name__ == "__main__":
    main()
