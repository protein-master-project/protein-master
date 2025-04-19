from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app import routes_api
from app import routes_web
from app import llm_agent_api
