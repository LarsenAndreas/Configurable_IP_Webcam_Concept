from flask import Flask, render_template, Response, request
from camera import Camera
import cv2

app = Flask(__name__)

cam = Camera()

@app.route('/')
def index():
    data = {
        'focus': -1 if cam.cam.get(cv2.CAP_PROP_AUTOFOCUS) else int(cam.cam.get(cv2.CAP_PROP_FOCUS)),
        'brightness': int(cam.cam.get(cv2.CAP_PROP_BRIGHTNESS)),
        'contrast': int(cam.cam.get(cv2.CAP_PROP_CONTRAST)),
        'saturation': int(cam.cam.get(cv2.CAP_PROP_SATURATION)),
    }
    return render_template('index.html', data=data)


@app.route('/change_cam_params', methods=("GET", "POST"))
def updateCamParams():
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
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # a = Camera()
    # print(a.cam.read())
    # tester()
