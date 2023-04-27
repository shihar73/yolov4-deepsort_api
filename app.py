from flask import Flask, request, jsonify
import cv2
from object_tracker import ObjectTracker # Import the ObjectTracker class from object_tracker.py file

app = Flask(__name__)

@app.route('/api/objects', methods=['POST'])
def count_objects():
    # Read the video file from the request
    video_file = request.files['video']
    video_bytes = video_file.read()

    # Convert the video bytes to numpy array
    video_nparray = np.fromstring(video_bytes, np.uint8)
    video = cv2.imdecode(video_nparray, cv2.IMREAD_COLOR)

    # Create an instance of the ObjectTracker class and pass the video to it
    tracker = ObjectTracker(video, 'yolov4', True)

    # Process the video using the YOLOv4 and Deep SORT models
    tracker.track_objects()

    # Count the number of objects detected
    num_objects = len(tracker.object_counts)

    # Return the response containing the number of objects
    response = {
        'num_objects': num_objects
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)