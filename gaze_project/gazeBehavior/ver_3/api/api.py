# import time
# from flask import Flask

# app = Flask(__name__, static_folder='../build', static_url_path='/')


# @app.route('/')
# def index():
#     return app.send_static_file('index.html')


# @app.route('/api/time')
# def get_current_time():
#     return {'time': time.time()}


# import os
# from flask import Flask, request, session
# from werkzeug.utils import secure_filename
# from flask_cors import CORS
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('HELLO WORLD')

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# app = Flask(__name__, static_folder='../build', static_url_path='/')
# app.config['UPLOAD_FOLDER'] = '../build'
# CORS(app, resources={r'*': {'origins': '*'}})


# @app.route('/build', methods=['POST'])
# def fileUpload():
#     target = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     logger.info("welcome to upload`")
#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     destination = "/".join([target, filename])
#     file.save(destination)
#     session['uploadFilePath'] = destination
#     response = "Whatever you wish too return"
#     return response

# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# if __name__ == "__main__":
#     app.secret_key = os.urandom(24)
#     app.run(debug=True, port=5000)



import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = './build'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='../build', static_url_path='/')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    print('in the upload_file!')
    if request.method == 'POST':
        f = request.files['image']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully!'

@app.route('/')
def index():
    return app.send_static_file('index.html')


CORS(app, resources={r'*': {'origins': '*'}})

# from flask import Flask, flash, request, redirect, url_for, session
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#         return 'Hello, world!'
# @app.route('/upload', methods=['GET','POST'])
# def upload_file():
#     print('in the upload_file!')
#     if request.method == 'POST':
#         f = request.files['image']
#         f.save(secure_filename(f.filename))
#         return 'file uploaded successfully!'

# if __name__ == '__main__':
#     app.run()