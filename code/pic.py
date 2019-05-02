#! usr/bin/env python 
import cv2
import numpy as np


img = cv2.imread('/home/hyungjun/project/golf/code/C004.png', 0)
drawing = False 

ix,iy = -1,-1

def draw_circle(event, x,y, flags, param):
    global ix,iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN: 
        drawing = True 
        ix, iy = x,y
        print(ix,iy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False             
        cv2.circle(img,(x,y),1,(0,255,0),-1)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while True:
	cv2.imshow('image', img)

	k = cv2.waitKey(1) & 0xFF

	
	if k == 27:        
        	break

cv2.destroyAllWindows()
