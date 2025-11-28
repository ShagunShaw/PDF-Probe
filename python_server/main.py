from flask import Flask, request, jsonify
from flask_cors import CORS

from vectors import create_vector, get_response

app = Flask(__name__)
CORS(app)  # enable CORS for all domains

first_question = True
vector_store = None

# Routes
@app.route("/")
def root():
    return jsonify({
        "message": "AI PDF Assistant API is running! 🚀",
        "status": "active"
    })

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"})

@app.route("/api/chat", methods=["POST"])
def chat():
    global first_question, vector_store

    try:
        data = request.get_json()
        page_url = data.get("page_url")
        question = data.get("question")

        if not question or not question.strip():
            return jsonify({"error": "Question cannot be empty"}), 400

        response = ""
        if first_question:
            first_question = False
            vector_store = create_vector(page_url)
            response = get_response(vector_store, question)
        else:
            response = get_response(vector_store, question)

        return jsonify({
            "response": response,
            "status": "success",
            "status_code": 200
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)