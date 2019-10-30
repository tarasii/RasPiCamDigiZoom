import serial
import numpy as np
import cv2

max_v = 26
min_v = 15

ser = serial.Serial ('com3')
ser.baudrate = 115200

if not ser.is_open:
  quit()

  
head = ser.read(10)

x = ser.read(2)
if x[0]<x[1]:
	x = ser.read(1)

x = ser.read(2)
z = int.from_bytes(x, "little")
while z < 10000:
	x = ser.read(2)
	z = int.from_bytes(x, "little")

while z > 10000:
	x = ser.read(2)
	z = int.from_bytes(x, "little")

#32*24*2=1536
while(True):
    # Capture frame-by-frame
	data = ser.read(1544)

	T_array0 = np.frombuffer(data, dtype=np.uint16)

	D = T_array0[:768]/100
	max_a = np.max(D)
	min_a = np.min(D)
	max_v = max(max_v, max_a)
	min_v = min(min_v, min_a)
	D.shape = (24,32)
	D = np.uint8((D-min_v)*255/(max_v-min_v))
	#D = np.uint8(255-(D-min_v)*255/(max_v-min_v))

	#img = cv2.applyColorMap(D, cv2.COLORMAP_JET)
	#img = cv2.applyColorMap(D, cv2.COLORMAP_COOL)
	img = cv2.applyColorMap(D, cv2.COLORMAP_HOT) #yelow red black
	#img = cv2.applyColorMap(D, cv2.COLORMAP_AUTUMN)
	#img = cv2.applyColorMap(D, cv2.COLORMAP_BONE) #black and white
	#img = cv2.applyColorMap(D, cv2.COLORMAP_RAINBOW) # for inv
	img = cv2.resize(img, (320,240), interpolation = cv2.INTER_LINEAR)
	#img = cv2.resize(img, (320,240), interpolation = cv2.INTER_CUBIC)
	#img = cv2.resize(img, (320,240), interpolation = cv2.INTER_LANCZOS4)
	img = cv2.flip(img, 1)
	cv2.imshow('Output', img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
ser.close()


