"""
FoxDot Code Executor - Safe execution environment for FoxDot code
Similar to code_executor.py but specialized for live music coding
"""

import sys
import io
import traceback
import datetime
import asyncio
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of FoxDot code execution."""
    success: bool
    code: str
    output: str = ""
    error: Optional[str] = None
    error_details: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    players_affected: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'code': self.code,
            'output': self.output,
            'error': self.error,
            'error_details': self.error_details,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp,
            'players_affected': self.players_affected,
            'warnings': self.warnings
        }


class FoxDotExecutor:
    """
    Execute FoxDot code in a controlled environment.
    Maintains the FoxDot runtime state across executions.
    """
    
    def __init__(self, max_execution_time: int = 30):
        """
        Initialize FoxDot executor.
        
        Args:
            max_execution_time: Maximum execution time in seconds
        """
        self.max_execution_time = max_execution_time
        self.execution_history: List[ExecutionResult] = []
        self.foxdot_initialized = False
        self.foxdot_env: Dict[str, Any] = {}
        
        # Callbacks
        self._on_play_callback: Optional[Callable] = None
        self._on_stop_callback: Optional[Callable] = None
        self._on_error_callback: Optional[Callable] = None
    
    def initialize_foxdot(self) -> bool:
        """
        Initialize FoxDot environment.
        Must be called before executing code.
        """
        if self.foxdot_initialized:
            return True
        
        try:
            logger.info("[FOXDOT_EXECUTOR] Initializing FoxDot...")
            
            # Import FoxDot
            import FoxDot
            from FoxDot import Clock, Scale, Root, Player, Group
            
            # Get all FoxDot exports
            self.foxdot_env = {
                name: getattr(FoxDot, name) 
                for name in dir(FoxDot) 
                if not name.startswith('_')
            }
            
            # Ensure key objects are available
            self.foxdot_env['Clock'] = Clock
            self.foxdot_env['Scale'] = Scale
            self.foxdot_env['Root'] = Root
            self.foxdot_env['Player'] = Player
            self.foxdot_env['Group'] = Group
            
            # Add standard library helpers
            self.foxdot_env['print'] = print
            self.foxdot_env['range'] = range
            self.foxdot_env['len'] = len
            self.foxdot_env['list'] = list
            self.foxdot_env['int'] = int
            self.foxdot_env['float'] = float
            self.foxdot_env['str'] = str
            
            self.foxdot_initialized = True
            logger.info("[FOXDOT_EXECUTOR] FoxDot initialized successfully!")
            logger.info("[FOXDOT_EXECUTOR] Make sure SuperCollider is running with FoxDot.start")
            
            return True
            
        except ImportError as e:
            logger.error(f"[FOXDOT_EXECUTOR] FoxDot not installed: {e}")
            logger.error("[FOXDOT_EXECUTOR] Install with: pip install FoxDot")
            return False
            
        except Exception as e:
            logger.error(f"[FOXDOT_EXECUTOR] Error initializing FoxDot: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def set_callbacks(
        self,
        on_play: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """Set callbacks for execution events."""
        self._on_play_callback = on_play
        self._on_stop_callback = on_stop
        self._on_error_callback = on_error
    
    def _extract_players_from_code(self, code: str) -> List[str]:
        """Extract player names from FoxDot code."""
        import re
        
        players = []
        
        # Match player assignments: p1 >> synth(...)
        player_pattern = r'([a-zA-Z]\w*)\s*>>'
        matches = re.findall(player_pattern, code)
        players.extend(matches)
        
        # Match .stop() calls
        stop_pattern = r'([a-zA-Z]\w*)\.stop\(\)'
        stops = re.findall(stop_pattern, code)
        players.extend(stops)
        
        return list(set(players))
    
    def execute(self, code: str, explanation: Optional[str] = None) -> ExecutionResult:
        """
        Execute FoxDot code synchronously.
        
        Args:
            code: FoxDot Python code to execute
            explanation: Optional description of what the code does
            
        Returns:
            ExecutionResult with execution details
        """
        logger.info(f"[FOXDOT_EXECUTOR] Executing code...")
        if explanation:
            logger.info(f"[EXPLANATION] {explanation}")
        
        result = ExecutionResult(
            success=False,
            code=code,
            players_affected=self._extract_players_from_code(code)
        )
        
        start_time = datetime.datetime.now()
        
        # Initialize FoxDot if needed
        if not self.foxdot_initialized:
            if not self.initialize_foxdot():
                result.error = "FoxDot not initialized. Make sure FoxDot and SuperCollider are installed."
                if self._on_error_callback:
                    self._on_error_callback(result)
                return result
        
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Execute the code
            exec(code, self.foxdot_env)
            
            # Capture output
            stdout_output = sys.stdout.getvalue()
            stderr_output = sys.stderr.getvalue()
            
            result.output = stdout_output if stdout_output else stderr_output
            result.success = True
            
            # Check for Clock.clear() to trigger stop callback
            if 'Clock.clear()' in code:
                if self._on_stop_callback:
                    self._on_stop_callback()
            elif result.players_affected and self._on_play_callback:
                self._on_play_callback(result.players_affected)
            
        except Exception as e:
            error_traceback = traceback.format_exc()
            result.error = str(e)
            result.error_details = error_traceback
            result.output = sys.stderr.getvalue()
            
            logger.error(f"[EXECUTION_ERROR] {str(e)}")
            
            if self._on_error_callback:
                self._on_error_callback(result)
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        # Calculate execution time
        execution_time = (datetime.datetime.now() - start_time).total_seconds()
        result.execution_time = execution_time
        
        if execution_time > self.max_execution_time:
            result.warnings.append(
                f"Execution time ({execution_time:.2f}s) exceeded recommended limit ({self.max_execution_time}s)"
            )
        
        # Store in history
        self.execution_history.append(result)
        
        return result
    
    async def execute_async(self, code: str, explanation: Optional[str] = None) -> ExecutionResult:
        """
        Execute FoxDot code asynchronously.
        
        Args:
            code: FoxDot Python code to execute
            explanation: Optional description
            
        Returns:
            ExecutionResult with execution details
        """
        # Run synchronous execute in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.execute, code, explanation)
    
    def stop_all(self) -> ExecutionResult:
        """Stop all FoxDot players."""
        return self.execute("Clock.clear()", "Stop all music")
    
    def set_tempo(self, bpm: int) -> ExecutionResult:
        """Set the tempo."""
        return self.execute(f"Clock.bpm = {bpm}", f"Set tempo to {bpm} BPM")
    
    def set_scale(self, scale: str) -> ExecutionResult:
        """Set the default scale."""
        return self.execute(f"Scale.default = Scale.{scale}", f"Set scale to {scale}")
    
    def set_root(self, root: str) -> ExecutionResult:
        """Set the root note."""
        return self.execute(f'Root.default = "{root}"', f"Set root note to {root}")
    
    def stop_player(self, player_name: str) -> ExecutionResult:
        """Stop a specific player."""
        return self.execute(f"{player_name}.stop()", f"Stop player {player_name}")
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        Validate FoxDot code without executing it.
        Checks syntax and basic structure.
        
        Returns:
            Dict with 'valid', 'errors', 'warnings' keys
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'detected_players': [],
            'detected_synths': []
        }
        
        import re
        
        # Check Python syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            result['valid'] = False
            result['errors'].append(f"Syntax error at line {e.lineno}: {e.msg}")
            return result
        
        # Extract players and synths
        player_pattern = r'(\w+)\s*>>\s*(\w+)\s*\('
        matches = re.findall(player_pattern, code)
        
        for player, synth in matches:
            result['detected_players'].append(player)
            result['detected_synths'].append(synth)
        
        # Check for common issues
        if 'import ' in code.lower():
            result['warnings'].append("Import statements may not be needed - FoxDot provides most functions")
        
        # Check for infinite loops
        if 'while True' in code or 'while 1' in code:
            result['warnings'].append("Detected potential infinite loop - FoxDot uses Clock for timing")
        
        return result
    
    def get_available_synths(self) -> List[str]:
        """Get list of available synths."""
        if not self.foxdot_initialized:
            self.initialize_foxdot()
        
        if 'SynthDefs' in self.foxdot_env:
            return list(self.foxdot_env['SynthDefs'])
        return []
    
    def get_execution_history(self, limit: int = 10) -> List[ExecutionResult]:
        """Get recent execution history."""
        return self.execution_history[-limit:]
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history.clear()


# Module-level singleton
_executor: Optional[FoxDotExecutor] = None


def get_executor() -> FoxDotExecutor:
    """Get or create the FoxDot executor singleton."""
    global _executor
    if _executor is None:
        _executor = FoxDotExecutor()
    return _executor


def execute_foxdot_code(code: str, explanation: Optional[str] = None) -> ExecutionResult:
    """
    Convenience function to execute FoxDot code.
    
    Args:
        code: FoxDot Python code
        explanation: Optional description
        
    Returns:
        ExecutionResult
    """
    executor = get_executor()
    return executor.execute(code, explanation)


async def execute_foxdot_code_async(code: str, explanation: Optional[str] = None) -> ExecutionResult:
    """
    Async convenience function to execute FoxDot code.
    
    Args:
        code: FoxDot Python code
        explanation: Optional description
        
    Returns:
        ExecutionResult
    """
    executor = get_executor()
    return await executor.execute_async(code, explanation)


def format_execution_result(result: ExecutionResult) -> str:
    """Format execution result for display."""
    output_parts = []
    
    if result.success:
        output_parts.append("✓ **Execution Successful**")
    else:
        output_parts.append("✗ **Execution Failed**")
    
    output_parts.append("\n**Code:**")
    output_parts.append(f"```python\n{result.code}\n```")
    
    if result.output:
        output_parts.append("\n**Output:**")
        output_parts.append(f"```\n{result.output}\n```")
    
    if result.error:
        output_parts.append("\n**Error:**")
        output_parts.append(f"```\n{result.error}\n```")
    
    if result.players_affected:
        output_parts.append(f"\n**Players:** {', '.join(result.players_affected)}")
    
    output_parts.append(f"\n*Execution time: {result.execution_time:.3f}s*")
    
    return "\n".join(output_parts)


if __name__ == "__main__":
    # Test the executor
    print("Testing FoxDot Executor...")
    print("=" * 50)
    
    executor = FoxDotExecutor()
    
    # Test validation
    test_code = """
Clock.bpm = 120
Scale.default = Scale.minor
p1 >> pluck([0, 2, 4, 7], dur=1)
d1 >> play("x-o-")
"""
    
    print("Validating code...")
    validation = executor.validate_code(test_code)
    print(f"Valid: {validation['valid']}")
    print(f"Players: {validation['detected_players']}")
    print(f"Synths: {validation['detected_synths']}")
    
    # Test execution (will only work if FoxDot is installed)
    print("\nAttempting execution...")
    result = executor.execute(test_code)
    print(format_execution_result(result))
