from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
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
            if data:
                clip = VideoFileClip("./static/output/tracker.avi")
                clip.write_videofile("./static/output/tracker.mp4")
                
            print(v_file, data["count"])
            return render_template('index.html', filename=data["filename"], count=data["count"])

    # Render the video upload form and the video player together
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)