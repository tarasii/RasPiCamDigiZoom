import serial
import numpy as np
import cv2
import matplotlib.pyplot as plt

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
data = ser.read(1544)

T_array0 = np.frombuffer(data, dtype=np.uint16)
#np.save("ir_sample3", T_array0)

#plt.plot(T_array0)
#plt.show()

D = T_array0[:768]/100
max_v = np.max(D)
min_v = np.min(D)
D.shape = (24,32)
D = np.uint8((D-min_v)*255/(max_v-min_v))

img = cv2.applyColorMap(D, cv2.COLORMAP_JET)
img = cv2.resize(img, (320,240), interpolation = cv2.INTER_LINEAR)
img = cv2.flip(img, 1)
cv2.imshow('Output', img)
cv2.waitKey(0)


cv2.destroyAllWindows()
ser.close()


