from flask import *
from flask_cors import CORS

# @app.route('/api/getstimuli', methods=['POST'])
# def stimuliInfo():
#   print("/api/getstimuli")
#   print(request.form)
#   response = {}
#   try:

#   except Exception as e:

app = Flask(__name__)
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True)
CORS(app)
