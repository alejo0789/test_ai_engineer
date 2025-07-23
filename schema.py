def validate_query_request(data):
    if not data:
        return "Missing JSON body."
    if "user_id" not in data or not isinstance(data["user_id"], str) or not data["user_id"].strip():
        return "Invalid or missing 'user_id'."
    if "query" not in data or not isinstance(data["query"], str) or not data["query"].strip():
        return "Invalid or missing 'query'."
    return None
