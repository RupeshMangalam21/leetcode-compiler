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
        return {"error": f"Unsupported language: {language}"}

    # Generate a unique filename for the code to avoid conflicts
    unique_id = str(uuid.uuid4())
    filename, docker_dir = file_map[language]
    unique_filename = f"{unique_id}_{filename}"

    # Write code to file
    with open(unique_filename, "w") as f:
        f.write(code)

    # Build and run the Docker container
    try:
        subprocess.run(f"docker build -t {language}_executor {docker_dir}", shell=True, check=True)
        result = subprocess.run(f"docker run --rm -v {os.path.abspath(os.getcwd())}:/app {language}_executor {unique_filename}", shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
    except subprocess.CalledProcessError as e:
        return {"error": f"Error during Docker execution: {str(e)}"}
    finally:
        # Cleanup the generated file
        if os.path.exists(unique_filename):
            os.remove(unique_filename)

    return {"output": output or "No output"}
