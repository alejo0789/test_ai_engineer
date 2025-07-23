from flask import Flask, request, jsonify
from schema import validate_query_request
from agent_controller import handle_query

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.get_json()
    error = validate_query_request(data)
    
    if error:
        return jsonify({"error": error}), 400

    user_id = data["user_id"]
    query = data["query"]

    reply = handle_query(user_id, query)
    return jsonify({"reply": reply}), 200

if __name__ == '__main__':
    app.run(debug=True)
