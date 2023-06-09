from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from object_tracker import run
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']





@app.route('/', methods=['GET', 'POST'])
def count_objects():
    if request.method == 'POST':
        # Handle video upload
        video = request.files['video']
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            v_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(v_file)
            data = run(v_file)
            print(data)
            return render_template('index.html', count=data["count"], cars=data["cars"],bicycles=data["bicycles"],persons=data["persons"])

    # Render the video upload form and the video player together
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)