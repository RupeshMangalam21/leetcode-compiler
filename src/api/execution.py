import subprocess
import os
import uuid

def execute_code(code: str, language: str) -> dict:
    file_map = {
        "python": ("script.py", "docker/python"),
        "nodejs": ("script.js", "docker/nodejs"),
        "cpp": ("script.cpp", "docker/cpp"),
        "java": ("Main.java", "docker/java")
    }

    if language not in file_map:
        return {"status": "failure", "error": f"Unsupported language: {language}"}

    unique_id = str(uuid.uuid4())
    filename, docker_dir = file_map[language]
    unique_filename = f"{unique_id}_{filename}"
    output = ""

    # Create the temporary file
    try:
        with open(unique_filename, "w") as f:
            f.write(code)

        # Run the Docker container
        print(f"Running Docker container for {language} code execution...")
        result = subprocess.run(
            f"docker run --rm -v {os.path.abspath(os.getcwd())}:/app {language}_executor {unique_filename}",
            shell=True,
            capture_output=True,
            text=True
        )

        # Capture the output
        if result.returncode == 0:
            output = result.stdout
            status = "success"
        else:
            output = f"Error: {result.stderr}"
            status = "failure"

    except subprocess.CalledProcessError as e:
        return {"status": "failure", "error": f"Docker execution error: {str(e)}"}
    finally:
        # Cleanup temporary file
        if os.path.exists(unique_filename):
            os.remove(unique_filename)

    return {"status": status, "output": output or "No output"}
