import cv2
import numpy as np
from datetime import datetime as dt

class cl():
    white = (255, 255, 255)
    black = (0,0,0)


class cl_xy(object):
    """docstring for xy"""
    def __init__(self, x, y):
        super(cl_xy, self).__init__()
        self.x = x
        self.y = y

    def point():
        return (self.x, self.y)
        

class cl_sz(object):
    """docstring for sz"""
    def __init__(self, img, zoom):
        super(cl_sz, self).__init__()

        self.height = len(img)
        self.width = len(img[0])

        #self.max = cl_xy(self.width, self.height);
        #self.center = cl_xy(self.width / 2, self.height / 2);
        self.output = cl_xy(320, 240);
        self.max = cl_xy(self.output.x, self.output.y);
        self.center = cl_xy(self.max.x / 2, self.max.y / 2);
        

        self.margin = cl_xy(50, 50) 
        self.center_margin = cl_xy(2, 2) 
        self.center_padding = cl_xy(10, 10) 

        self.sizes = (
            (320, 240, "1x"),
            (480, 360, "1.5x"),
            (640, 480, "2x"),
            )

        self.zoom(zoom)
        self.calc_aim()


    def zoom(self, val):
        #self.calc_aim();
        self.input_center = cl_xy(self.sizes[zoom][0] / 2, self.sizes[zoom][1] / 2);
        self.input_max = cl_xy(self.sizes[zoom][0], self.sizes[zoom][1]);

        self.zooms = (
            (0,240, 0, 320),
            (self.input_center.y-240/2, self.input_center.y+240/2, self.input_center.x-320/2, self.input_center.x+320/2),
            (self.input_center.y-240/2, self.input_center.y+240/2, self.input_center.x-320/2, self.input_center.x+320/2),
            )


    def calc_aim(self):
        self.aim_lines = ( 
            ((self.margin.x, self.center.y), (self.center.x - self.center_padding.x, self.center.y), cl.white), #left
            ((self.center.x + self.center_padding.x, self.center.y), (self.max.x - self.margin.x, self.center.y), cl.white), #right
            ((self.center.x, self.max.y - self.margin.y), (self.center.x, self.center.y + self.center_padding.y),cl.white), #bottom
            ((self.center.x - self.center_margin.x, self.center.y), (self.center.x + self.center_margin.x, self.center.y), cl.white), #cross x
            ((self.center.x, self.center.y - self.center_margin.y), (self.center.x, self.center.y + self.center_margin.y), cl.white) #cross y
        )

def draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    #cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

def draw_aim_simple(img):
    img_height = len(img)
    img_width = len(img[0])
    centr_x = img_width / 2
    centr_y = img_height / 2
    margin_x = 50
    margin_y = 50

    color_white = (255, 255, 255)
    cv2.line(frame, (margin_x, centr_y),
        (img_width - margin_x, centr_y),
        cl.white)
    cv2.line(frame, (centr_x, margin_y),
        (centr_x, img_height - margin_y),
        cl.white)


def draw_aim(img, sz):

    for p0, p1, color in sz.aim_lines:
        cv2.line(frame, p0, p1, color)



# Playing video from file:
# cap = cv2.VideoCapture('vtest.avi')
# Capturing video from webcam:
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

zoom = 0
ret, frame = cap.read()
sz = cl_sz(frame, zoom)

print(sz.zooms[zoom])

prew_time = dt.now()
fps = 0

currentFrame = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)

    frame = cv2.resize(frame, (sz.sizes[zoom][0], sz.sizes[zoom][1]), interpolation = cv2.INTER_AREA)
    #if (sz.zooms[zoom][1]<>sz.zooms[zoom][4]):
    frame = frame[sz.zooms[zoom][0]:sz.zooms[zoom][1], sz.zooms[zoom][2]:sz.zooms[zoom][3]]

    cur_time = dt.now()
    delta = cur_time - prew_time
    if (delta.seconds >= 1):
        fps = currentFrame
        currentFrame = 0
        prew_time = cur_time

    draw_label(frame, '{}'.format(cur_time), (20,20), (125,125,0))
    draw_label(frame, 'in:{}x{}; out:{}x{}; fps:{}; {}'.format(sz.input_max.x, sz.input_max.y, sz.max.x, sz.max.y, fps, sz.sizes[zoom][2]), (20,40), (125,125,0))

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Saves image of the current frame in jpg file
    # name = 'frame' + str(currentFrame) + '.jpg'
    # cv2.imwrite(name, frame)

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    draw_aim(frame, sz)

    cv2.imshow('frame',frame)

    # To stop duplicate images
    currentFrame += 1

    kk = cv2.waitKey(1)
    if kk == ord('z'):
        zoom += 1
        if zoom >= len(sz.zooms):
            zoom = 0;
        sz.zoom(zoom)
        print(zoom)
    
    if kk == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
