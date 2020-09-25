from flask import *
from flask_cors import CORS

app = Flask(__name__)
if __name__ == '__main__':  
  app.run(debug=True, port=5001)
CORS(app)
