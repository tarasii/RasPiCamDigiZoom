import cv2
import numpy as np
from datetime import datetime as dt
import cvhelper

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

zooms = ((160,120), (320,240), (480, 360), (640,480), (800,600), (1280,720), (1600,1200))

zoom = 0;
w, h = zooms[zoom]
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #1600
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h) #1200

prew_time, frame_cnt, fps = dt.now(), 0, 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cur_time = dt.now()
    delta = cur_time - prew_time
    if (delta.seconds >= 1):
        fps = frame_cnt / delta.seconds

    frame_cnt += 1

    cvhelper.draw_label(frame, '{}'.format(cur_time), (20,20), (125,125,0))
    cvhelper.draw_label(frame, 'in:{}x{}; fps:{};'.format(w, h, fps), (20,40), (125,125,0))

    cv2.imshow('frame', frame)

    kk = cv2.waitKey(1)
    if kk == ord('z'):
        zoom += 1
        if zoom >= len(zooms):
            zoom = 0;
        
        prew_time = dt.now()
        frame_cnt = 0

        w, h = zooms[zoom]
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w) #1600
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h) #1200

        #sleep(1)
        ret, frame = cap.read()
        print(zoom, np.shape(frame))
    
    if kk == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
