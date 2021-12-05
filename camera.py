import cv2

# This is the main camera object. This is configured to work on a creative livecam.
# The setting for an abitrary camera might differ. The same with the values. For a list of
# possible settings see https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html

class Camera():

    def __init__(self):
        self.cam = cv2.VideoCapture(-1) # Change to 0 if it does not work

    def get_frame(self):
        _, img = self.cam.read()
        img = img[60:-60] # Crops off black borders
        self.frame = cv2.imencode('.jpg', img)[1].tobytes()
        return self.frame

    def autofocus(self, val):
        """ val = bool"""
        self.cam.set(cv2.CAP_PROP_AUTOFOCUS, val)
    
    def focus(self, val):
        """ val = int [0, 27]"""
        self.cam.set(cv2.CAP_PROP_FOCUS, val)
    
    def brightness(self, val):
        """ val = int [-64, 64]"""
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, val)
    
    def contrast(self, val):
        """ val = int [0, 90]"""
        self.cam.set(cv2.CAP_PROP_CONTRAST, val)

    def staturation(self, val):
        """ val = int [50, 120]"""
        self.cam.set(cv2.CAP_PROP_SATURATION, val)

    def hue(self, val):
        """ val = """
        self.cam.set(cv2.CAP_PROP_HUE, val)

    def exposure(self, val):
        """ val = """
        self.cam.set(cv2.CAP_PROP_EXPOSURE, val)

    def temperature(self, val):
        """ val = """
        self.cam.set(cv2.CAP_PROP_TEMPERATURE, val)




        