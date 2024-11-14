import os
from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Enable flash messages
app.secret_key = os.urandom(24)

# HTML template
HTML = '''
<!doctype html>
<html>
<head>
    <title>File Upload and Download</title>
</head>
<body>
    <h1>File Upload and Download</h1>
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="flashes">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <h2>Uploaded Files</h2>
    <ul>
    {% for file in files %}
        <li><a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully')
            return redirect(url_for('upload_file'))
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    
    # Get list of uploaded files
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML, files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)