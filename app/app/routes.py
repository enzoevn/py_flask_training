from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from flask import jsonify
from werkzeug.security import check_password_hash
import requests
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'app/app/static/uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

users = {
    "test@example.com": {
        "password": "password123",
        "name": "Test User"
    },
    "jdoe@example.com": {
        "password": "jdoe2021",
        "name": "John Doe"
    }
}


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    user.name = users[email]['name']   
    return user

@app.route('/')
#@login_required
def home():
    return render_template('index.html', user=current_user)

# @app.route('/webapp')
# @login_required
# def webapp():
#     response = requests.get('http://172.17.0.3:6006')
#     data = response.json()  # Convert the response to a Python dictionary
#     return render_template('app.html', user=current_user, data=data)

@app.route('/resume')
def resume():
    return render_template('resume.html', user=current_user)

@app.route('/projects')
def projects():
    return render_template('projects.html', user=current_user)

@app.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # security check
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
    # Hashed password check with werkzeug
    username = request.form.get('username')
    password = request.form.get('password')

    if check_password_hash(users[username]['password'], password):        
        return 'error', 401    

    user = User()
    user.id = username
    login_user(user)
    return 'success', 200
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['image']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basically show on the browser the uploaded file
            return redirect(url_for('upload'))

    # Get list of files in the upload directory
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return render_template('app.html', images=images)

@app.route('/static/<filename>')
def uploaded_file(filename):
    filename = secure_filename(filename)    
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return redirect(url_for('upload'))
    else:
        return "Error: file not found."
    
def send_image_to_api(image_path):
    url = "http://172.17.0.3:6006"  # Replace with your API URL
    
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()  # If the API returns JSON data
    else:
        return None


@app.route('/send_to_api/<filename>', methods=['POST'])
def send_to_api(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        response = send_image_to_api(filepath)
        print(response)
        if response is not None:
            # Store the response in the session
            session[filename] = response['prediction']
        else:
            session[filename] = "Error: could not send image to API."
    else:
        session[filename] = "Error: file not found."

    return redirect(url_for('upload')) 
