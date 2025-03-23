from app import app
import os

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
