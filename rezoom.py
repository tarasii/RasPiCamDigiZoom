import cv2
import numpy as np
from datetime import datetime as dt
import cvhelper


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


xout = 320
yout = 240
zooms = ((320,240,"1x"), (480, 360, "1.5x"), (640,480,"2x"), (800,600,"2.5x"), (1280,720,"3x"))
cuts = ((0,0), (160,60), (160,120), (240,180), (480,240))


def calc_cuts(x_out, y_out):
    for x, y, z in zooms:
        print((x - x_out)/2, (y-y_out)/2, (x - x_out)/2+x_out, (y-y_out)/2+y_out)

#calc_cuts(320, 240) 

def calc_aim(x_out, y_out):
    margin = cvhelper.xy(50, 50); 
    margin = cvhelper.xy(50, 50) 
    center_margin = cvhelper.xy(2, 2) 
    center_padding = cvhelper.xy(10, 10) 
    max_ = cvhelper.xy(x_out, y_out);
    center = cvhelper.xy(max_.x / 2, max_.y / 2);

    aim_lines = ( 
        ((margin.x, center.y), (center.x - center_padding.x, center.y), cvhelper.colors.white), #left
        ((center.x + center_padding.x, center.y), (max_.x - margin.x, center.y), cvhelper.colors.white), #right
        ((center.x, max_.y - margin.y), (center.x, center.y + center_padding.y), cvhelper.colors.white), #bottom
        ((center.x - center_margin.x, center.y), (center.x + center_margin.x, center.y), cvhelper.colors.white), #cross x
        ((center.x, center.y - center_margin.y), (center.x, center.y + center_margin.y), cvhelper.colors.white) #cross y
    )
    return aim_lines

aim_lines = calc_aim(xout, yout)

zoom = 0;
w, h, z = zooms[zoom]
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #1600
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h) #1200
    
prew_time, frame_cnt, fps = dt.now(), 0, 0

while(True):
    # Capture frame-by-frame

    ret, frame = cap.read()
    x0,y0 = cuts[zoom]
    x1,y1 = x0+xout,y0+yout 
    frame = frame[y0:y1, x0:x1]

    cur_time = dt.now()
    delta = cur_time - prew_time
    if (delta.seconds >= 1):
        fps = frame_cnt / delta.seconds

    frame_cnt += 1

    cvhelper.draw_label(frame, '{}'.format(cur_time), (20,20), (125,125,0))
    cvhelper.draw_label(frame, 'in:{}x{}; out:{}x{}; fps:{}; zoom:{};'.format(w, h, xout, yout, fps, z), (20,40), (125,125,0))
    cvhelper.draw_lines(frame, aim_lines);

    cv2.imshow('frame', frame)


    kk = cv2.waitKey(1)
    if kk == ord('z'):
        zoom += 1
        if zoom >= len(zooms):
            zoom = 0;
        
        prew_time = dt.now()
        frame_cnt = 0

        w, h, z = zooms[zoom]
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #1600
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h) #1200

        print(zoom)
    
    if kk == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
