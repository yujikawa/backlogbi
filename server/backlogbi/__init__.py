from flask import Flask
from flask_cors import CORS


api = Flask(__name__)
CORS(api)


import backlogbi.views