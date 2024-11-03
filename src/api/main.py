from flask import Flask, request, jsonify
from api.execution import execute_code
from db.models import SessionLocal, User
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/execute', methods=['POST'])
def execute_code_endpoint():
    data = request.get_json()
    code = data.get("code")
    language = data.get("language")
    
    if not code or not language:
        return jsonify({"error": "Code and language are required"}), 400

    # Execute the code
    result = execute_code(code, language)
    return jsonify(result), 200

# def test_connection():
#     db = SessionLocal()
#     try:
#         # Example query to add a new user entry
#         new_user = User(username="test_user3", password="password1233")
#         db.add(new_user)
#         db.commit()
#         print("Database connection successful and entry added.")
#     except Exception as e:
#         print("Error:", e)
#     finally:
#         db.close()

if __name__ == '__main__':
        # test_connection()
    app.run(host='0.0.0.0', port=7000)  

