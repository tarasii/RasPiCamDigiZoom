import cv2
import numpy as np
from datetime import datetime as dt
import cvhelper


class cl_sz(object):
    """docstring for sz"""
    def __init__(self, img, zoom):
        super(cl_sz, self).__init__()

        self.height = len(img)
        self.width = len(img[0])

        self.output = cvhelper.xy(320, 240);
        self.max = cvhelper.xy(self.output.x, self.output.y);
        self.center = cvhelper.xy(self.max.x / 2, self.max.y / 2);
        
        self.margin = cvhelper.xy(50, 50) 
        self.center_margin = cvhelper.xy(2, 2) 
        self.center_padding = cvhelper.xy(10, 10) 

        self.sizes = (
            (320, 240, "1x"),
            (480, 360, "1.5x"),
            (640, 480, "2x"),
            (800, 600, "2.5x"),
            (960, 720, "3x"),
            (1280, 960, "4x"),
            (1600, 1200, "5x"),
            )

        self.zoom(zoom)
        self.calc_aim()


    def zoom(self, val):
        self.input_center = cvhelper.xy(self.sizes[zoom][0] / 2, self.sizes[zoom][1] / 2);
        self.input_max = cvhelper.xy(self.sizes[zoom][0], self.sizes[zoom][1]);
        self.zooms = (self.input_center.y-240/2, self.input_center.y+240/2, self.input_center.x-320/2, self.input_center.x+320/2)


    def calc_aim(self):
        self.aim_lines = ( 
            ((self.margin.x, self.center.y), (self.center.x - self.center_padding.x, self.center.y), cvhelper.colors.white), #left
            ((self.center.x + self.center_padding.x, self.center.y), (self.max.x - self.margin.x, self.center.y), cvhelper.colors.white), #right
            ((self.center.x, self.max.y - self.margin.y), (self.center.x, self.center.y + self.center_padding.y),cvhelper.colors.white), #bottom
            ((self.center.x - self.center_margin.x, self.center.y), (self.center.x + self.center_margin.x, self.center.y), cvhelper.colors.white), #cross x
            ((self.center.x, self.center.y - self.center_margin.y), (self.center.x, self.center.y + self.center_margin.y), cvhelper.colors.white) #cross y
        )


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


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) 
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720) 
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280) 

cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)          
cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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
    frame = frame[sz.zooms[0]:sz.zooms[1], sz.zooms[2]:sz.zooms[3]]

    cur_time = dt.now()
    delta = cur_time - prew_time
    if (delta.seconds >= 1):
        fps = currentFrame/delta.seconds


    cvhelper.draw_label(frame, '{}'.format(cur_time), (20,20), (125,125,0))
    cvhelper.draw_label(frame, 'in:{}x{}; out:{}x{}; fps:{}; {}'.format(sz.input_max.x, sz.input_max.y, sz.max.x, sz.max.y, fps, sz.sizes[zoom][2]), (20,40), (125,125,0))

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Saves image of the current frame in jpg file
    # name = 'frame' + str(currentFrame) + '.jpg'
    # cv2.imwrite(name, frame)

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    cvhelper.draw_lines(frame, sz.aim_lines)

    cv2.imshow('frame', frame)

    # To stop duplicate images
    currentFrame += 1

    kk = cv2.waitKey(1)
    if kk == ord('z'):
        zoom += 1
        if zoom >= len(sz.sizes):
            zoom = 0;
        sz.zoom(zoom)
        
        prew_time = dt.now()
        currentFrame = 0
        
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, sz.input_max.x) #1600
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, sz.input_max.y) #1200

        print(zoom)
    
    if kk == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
