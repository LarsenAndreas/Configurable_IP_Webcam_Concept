from flask import Flask, render_template, Response, request
from camera import Camera
import cv2

app = Flask(__name__)

cam = Camera()

@app.route('/')
def index():
    # Send the current webcam parameters to JS
    data = {
        'focus': -1 if cam.cam.get(cv2.CAP_PROP_AUTOFOCUS) else int(cam.cam.get(cv2.CAP_PROP_FOCUS)),
        'brightness': int(cam.cam.get(cv2.CAP_PROP_BRIGHTNESS)),
        'contrast': int(cam.cam.get(cv2.CAP_PROP_CONTRAST)),
        'saturation': int(cam.cam.get(cv2.CAP_PROP_SATURATION)),
    }
    return render_template('index.html', data=data)


@app.route('/change_cam_params', methods=("GET", "POST"))
def updateCamParams():
    # Gets the changes from JS and updates the "cam" object
    payload = request.get_json()
    print(payload)
    cam.focus(int(payload['focus']))
    cam.brightness(int(payload['brightness']))
    cam.contrast(int(payload['contrast']))
    cam.staturation(int(payload['saturation']))

    if int(payload['focus']) == -1:
        cam.autofocus(True)
    return "OK"


def gen(camera):
    # This gets the frame from the camera object and converts it to something displayable
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
# This is the video feed which is embedded in the html
def video_feed():
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Debug must be false to work on ubuntu 20 server... Don't know why.
    app.run(host='0.0.0.0', debug=False)
