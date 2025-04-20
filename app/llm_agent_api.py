from flask import request, jsonify, Response
import os
# 1. Import the OpenAI class and potentially error types
from openai import OpenAI, APIError
# Assuming 'app' is your Flask app instance defined elsewhere
# If this file is the main application file, you might initialize it like this:
# from flask import Flask
# app = Flask(__name__)
from app import app  # Assuming app is defined in app.py or similar
from rag import mol_script_rag

# 2. Initialize the OpenAI client (v1.0.0+)
# It's generally better to initialize the client once outside the request handler
# to avoid recreation on every request.
# Ensure the OPENAI_API_KEY environment variable is set.
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Optionally, add a check to ensure the API key was loaded
    if not client.api_key:
        print("Warning: OPENAI_API_KEY environment variable not set or empty.")
        # Depending on your application logic, you might raise an error
        # or take other actions here.
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None # Mark client initialization as failed

@app.route("/llm", methods=["POST"])
def chat():
    # Check if the client was initialized successfully
    if client is None:
        return jsonify({"error": "OpenAI client not initialized. Check API key and server logs."}), 503 # Service Unavailable

    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Invalid payload, missing 'messages'"}), 400

    print("Received payload:", data) # Keep the print for debugging purposes

    messages = data["messages"]

    try:
        # 3. Call the API using the new client method: client.chat.completions.create
        response = client.chat.completions.create(
            # Note: "gpt-4.1" might not be a standard model identifier.
            # You might need to use models like "gpt-4", "gpt-4-turbo", or "gpt-4o".
            # Using gpt-4o here as an example, as it's a current and capable model.
            model="gpt-4.1",
            messages=messages,
            temperature=0.7,
            max_tokens=1024 * 8
        )

        # 4. Access the response message
        # response.choices[0].message is a ChatCompletionMessage object (a Pydantic model)
        assistant_message_obj = response.choices[0].message

        # Convert the response message object (Pydantic model) to a dictionary
        # to match the expected format in the 'messages' list
        # (The input/output 'messages' list typically contains dictionaries)
        assistant_msg_dict = {
            "role": assistant_message_obj.role,
            "content": assistant_message_obj.content
        }

        # Append the assistant's reply dictionary to the list
        messages.append(assistant_msg_dict)

        # Return the updated list of messages
        return jsonify({"messages": messages})

    # 5. Update error handling (optional but recommended)
    except APIError as e:
        # Handle OpenAI API specific errors
        print(f"OpenAI API Error: {e}")
        # Try to return more specific error information and status code
        status_code = getattr(e, 'status_code', 500)
        error_type = getattr(e, 'type', "api_error")
        return jsonify({"error": f"OpenAI API Error: {str(e)}", "type": error_type}), status_code
    except Exception as e:
        # Handle other unexpected errors during the process
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500

@app.route("/rag", methods=["GET"])
def rag():
    print("Received RAG request")
    return Response(mol_script_rag.prompt,
                    mimetype="text/plain; charset=utf-8")