import json

def validate_query_request(data: dict):
    """
    Validates the incoming JSON data for the /query endpoint.

    Args:
        data (dict): The JSON payload from the request.

    Raises:
        ValueError: If the data is invalid or missing required fields.
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    user_id = data.get("user_id")
    query = data.get("query")

    if not user_id or not isinstance(user_id, str) or user_id.strip() == "":
        raise ValueError("Missing or invalid 'user_id'. It must be a non-empty string.")

    if not query or not isinstance(query, str) or query.strip() == "":
        raise ValueError("Missing or invalid 'query'. It must be a non-empty string.")

    # Return the stripped values to ensure no leading/trailing whitespace
    return {
        "user_id": user_id.strip(),
        "query": query.strip()
    }