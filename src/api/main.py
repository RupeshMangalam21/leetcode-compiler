from flask import Flask, request, jsonify
import sys
sys.path.append('/app/src')
from api.execution import execute_code
from db.models import SessionLocal, User
from rq import Queue
from redis import Redis

app = Flask(__name__)

# Redis connection
r = Redis(host='redis', port=6379)
q = Queue(connection=r)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Code Execution API"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/api/execute', methods=['POST'])
def execute_code_endpoint():
    data = request.get_json()
    code = data.get("code")
    language = data.get("language")
    
    if not code or not language:
        return jsonify({"status": "failure", "error": "Code and language are required"}), 400

    try:
        # Enqueue the task for the worker
        job_id = enqueue_code_execution(language, code)
        return jsonify({"status": "success", "job_id": job_id}), 200
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500

def enqueue_code_execution(language, code):
    job = q.enqueue(execute_code, code, language)
    return job.get_id()

@app.route('/job_status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    try:
        job = q.fetch_job(job_id)
        if not job:
            return jsonify({"status": "failure", "error": "Job not found"}), 404

        if job.is_finished:
            return jsonify({"status": "success", "result": job.result}), 200
        elif job.is_failed:
            return jsonify({"status": "failure", "error": "Job execution failed"}), 500
        else:
            return jsonify({"status": "pending"}), 202
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
