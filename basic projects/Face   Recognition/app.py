from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2
import os

app = Flask(__name__)

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize camera
camera = cv2.VideoCapture(0)  # Change to 1 if using an external webcam
if not camera.isOpened():
    print("❌ Error: Could not open camera")

# Ensure 'static' folder exists for saving images
if not os.path.exists('static'):
    os.makedirs('static')


def generate_frames():
    """Capture and stream video frames"""
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/face_status')
def face_status():
    """Check if a face is detected"""
    success, frame = camera.read()
    if not success:
        return jsonify({"status": "Camera Error ❌"})

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    status = "Face Detected ✅" if len(faces) > 0 else "No Face Detected ❌"
    return jsonify({"status": status})


@app.route('/capture_frame', methods=['POST'])
def capture_frame():
    """Capture and save an image"""
    success, frame = camera.read()
    if not success:
        return jsonify({"error": "Capture failed"}), 500

    image_path = "static/captured_face.jpg"
    cv2.imwrite(image_path, frame)
    return jsonify({"image_url": "/download_image"})


@app.route('/download_image')
def download_image():
    """Allow the user to download the captured image"""
    return send_file("static/captured_face.jpg", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
