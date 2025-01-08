import subprocess
import os
import tempfile
import time
import logging
from pathlib import Path
from typing import Dict, Any
import uuid
import shutil

# Configure logging
logger = logging.getLogger(__name__)

class CodeExecutionService:
    """Service for handling code execution in isolated containers"""

    LANGUAGE_CONFIGS = {
        "python": {"file_ext": ".py", "image": "python_executor"},
        "nodejs": {"file_ext": ".js", "image": "nodejs_executor"},
        "cpp": {"file_ext": ".cpp", "image": "cpp_executor"},
        "java": {"file_ext": ".java", "image": "java_executor"},
    }

    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix='leetcode_executor_'))
        self._setup_workspace()

    def _setup_workspace(self):
        """Initialize secure workspace"""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.temp_dir, 0o755)

        try:
            # Copy required files for Java execution
            script_path = Path("/usr/local/bin/compile_and_run.sh")
            policy_path = Path("/app/java.policy")
            
            # Debugging: Check if the files exist before copying
            if not script_path.exists():
                logger.error(f"Script file not found: {script_path}")
            if not policy_path.exists():
                logger.error(f"Policy file not found: {policy_path}")

            shutil.copy(script_path, self.temp_dir / "compile_and_run.sh")
            shutil.copy(policy_path, self.temp_dir / "java.policy")
            os.chmod(self.temp_dir / "compile_and_run.sh", 0o755)
        except Exception as e:
            logger.error(f"Failed to copy required files: {e}")

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
                return {"status": "failure", "error": f"Unsupported language: {language}"}

            config = self.LANGUAGE_CONFIGS[language]
            file_name = "Main" if language == "java" else "script"
            temp_file = self.temp_dir / f"{file_name}{config['file_ext']}"
            temp_file.write_text(code)
            os.chmod(temp_file, 0o644)

            # Debugging logs to check if the file exists and its contents
            if temp_file.exists():
                logger.info(f"Source file created successfully: {temp_file}")
                logger.info(f"File content:\n{temp_file.read_text()}")
            else:
                logger.error(f"Source file {temp_file} was not created!")

            # Adjusted command with ls to check /app contents
            if language == "java":
                command = [
                    "docker", "run",
                    "--rm",
                    "--memory=512m",
                    "--cpus=1",
                    "--pids-limit=50",
                    "--security-opt=no-new-privileges",
                    "--cap-drop=ALL",
                    "-v", f"{self.temp_dir.absolute()}:/app:rw",
                    "--workdir=/app",
                    config["image"],
                    "sh", "-c", "ls -l /app && /app/compile_and_run.sh /app/Main.java"
                ]
            else:
                # Handle other languages like python, nodejs, cpp here
                command = [
                    "docker", "run",
                    "--rm",
                    "--memory=512m",
                    "--cpus=1",
                    "--pids-limit=50",
                    "--security-opt=no-new-privileges",
                    "--cap-drop=ALL",
                    "-v", f"{self.temp_dir.absolute()}:/app:rw",
                    "--workdir=/app",
                    config["image"],
                    "sh", "-c", "ls -l /app && ./compile_and_run.sh"
                ]

            logger.info(f"Executing code: id={execution_id}, language={language}")
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

            execution_time = time.time() - start_time
            response = {
                "status": "success" if result.returncode == 0 else "failure",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.stderr else None,
                "execution_time": execution_time,
                "execution_id": execution_id,
            }

            logger.info(f"Execution completed: id={execution_id}, status={response['status']}")
            return response

        except subprocess.TimeoutExpired:
            logger.error(f"Code execution timed out: id={execution_id}")
            return {"status": "timeout", "error": "Execution timed out", "execution_id": execution_id}

        except Exception as e:
            logger.error(f"Execution failed: id={execution_id}", exc_info=True)
            return {"status": "error", "error": str(e), "execution_id": execution_id}

        finally:
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception as e:
                    logger.error(f"Failed to delete temp file: {e}")

    def cleanup(self):
        """Clean up temporary resources"""
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

executor_service = CodeExecutionService()

def execute_code(code: str, language: str) -> Dict[str, Any]:
    """Main execution interface"""
    return executor_service.execute_code(code, language)