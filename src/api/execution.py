import subprocess
import os
import tempfile
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import uuid

# Configure logging to work with existing system
logger = logging.getLogger(__name__)

class CodeExecutionService:
    """Service for handling code execution in isolated containers"""
    
    LANGUAGE_CONFIGS = {
        "python": {
            "file_ext": ".py",
            "image": "python_executor"
        },
        "nodejs": {
            "file_ext": ".js",
            "image": "nodejs_executor"
        },
        "cpp": {
            "file_ext": ".cpp",
            "image": "cpp_executor"
        },
        "java": {
            "file_ext": ".java",
            "image": "java_executor"
        }
    }

    def __init__(self):
        self.execution_count = 0
        self.temp_dir = Path(tempfile.mkdtemp(prefix='leetcode_executor_'))
        self._setup_workspace()

    def _setup_workspace(self):
        """Initialize secure workspace"""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.temp_dir, 0o755)

    def execute_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Execute code in a secure Docker container
        
        Args:
            code: Source code to execute
            language: Programming language
            
        Returns:
            Dict containing execution results
        """
        execution_id = str(uuid.uuid4())
        start_time = time.time()
        temp_file = None

        try:
            if language not in self.LANGUAGE_CONFIGS:
                return {
                    "status": "failure",
                    "error": f"Unsupported language: {language}"
                }

            # Create source file
            config = self.LANGUAGE_CONFIGS[language]
            temp_file = self.temp_dir / f"script{config['file_ext']}"
            temp_file.write_text(code)
            os.chmod(temp_file, 0o644)

            # Prepare Docker command with security constraints
            command = [
                "docker", "run",
                "--rm",
                "--memory=512m",
                "--cpus=1",
                "--pids-limit=50",
                "--security-opt=no-new-privileges",
                "--cap-drop=ALL",
                "-v", f"{self.temp_dir}:/app:ro",
                "--workdir=/leetcode_compiler",
                config["image"],
                str(temp_file.name)
            ]

            # Execute code
            logger.info(f"Executing code: id={execution_id}, language={language}")
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

            execution_time = time.time() - start_time
            
            # Format result
            response = {
                "status": "success" if result.returncode == 0 else "failure",
                "output": result.stdout,
                "error": result.stderr if result.stderr else None,
                "execution_time": execution_time,
                "execution_id": execution_id
            }

            logger.info(
                f"Code execution completed: id={execution_id}, "
                f"status={response['status']}, "
                f"time={execution_time:.2f}s"
            )

            return response

        except subprocess.TimeoutExpired:
            logger.error(f"Code execution timed out: id={execution_id}")
            return {
                "status": "timeout",
                "error": "Execution timed out after 30 seconds",
                "execution_id": execution_id
            }

        except Exception as e:
            logger.error(f"Code execution failed: id={execution_id}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "execution_id": execution_id
            }

        finally:
            # Cleanup
            try:
                if temp_file and temp_file.exists():
                    temp_file.unlink()
            except Exception as e:
                logger.error(f"Failed to cleanup temp file: {e}")

    def cleanup(self):
        """Clean up temporary resources"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

# Singleton instance for the application
executor_service = CodeExecutionService()

def execute_code(code: str, language: str) -> Dict[str, Any]:
    """
    Main execution interface that can be imported by other modules
    
    Args:
        code: Source code to execute
        language: Programming language
        
    Returns:
        Dict containing execution results
    """
    return executor_service.execute_code(code, language)