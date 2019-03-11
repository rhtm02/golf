#! usr/bin/env python 

import cv2
import numpy as np
import io
import math
import glob

class Golf:
	def __init__(self, MP4):
		self.NAME = MP4
		#0,1,2 Not,Hit,Hole in
		self.classify = 0
		
		self.cap = cv2.VideoCapture(MP4)
		if(not self.cap.isOpened()):
			print('not open')

		self.height, self.width = (int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

		self.bgMog2 = cv2.createBackgroundSubtractorMOG2(varThreshold = 25, detectShadows = False)

		print(self.NAME)		
		self.AREA_TH = 80 #area threshold 
		self.CENTER_X = 301
		self.CENTER_Y = 204
		#361,256

	def check_hit(self,x,y, rad):
		if(math.sqrt((x)**2 + (y)**2) <= (math.sqrt((self.CENTER_X - 319)**2+(self.CENTER_Y - 204)**2) + rad)):
			print("hit")
			self.classify = 1
	def check_hole_in(self, lst_x, lst_y):
		if (math.sqrt(lst_x[-1]**2 + lst_y[-1]**2) < math.sqrt((self.CENTER_X - 319)**2 + (self.CENTER_Y - 204)**2)):
			self.classify = 2
	
	def findObjectAndDraw(self,bimage, src, lst_x, lst_y, t):
		res = src.copy()
		bimage = cv2.erode(bimage, None, 5)
		bimage = cv2.dilate(bimage, None, 5)
		bimage = cv2.erode(bimage, None, 7)
		_,contours,_ = cv2.findContours(bimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(src, contours, -1, (255,0,0),1)
		for i,cnt in enumerate(contours):
			area = cv2.contourArea(cnt)
			if area > self.AREA_TH:
				(x,y),rad = cv2.minEnclosingCircle(cnt)
				x = int(x) - self.CENTER_X
				y = self.CENTER_Y - int(y)  
				rad = int(rad)
				#print(rad)
				cv2.circle(res, (x,y),rad, (0,255,0),)
				#print('(x,y) = (%d, %d)'%(x,y))
				if(rad < 15):
					self.check_hit(x,y,rad)
				if (t >= 30):
					if (len(lst_x) != 0)  and ((lst_x[-1] == x) and (lst_y[-1] == y)):
						continue
					else:
						lst_x.append(x)
						lst_y.append(y)
		return res, lst_x,lst_y

	def Perspective(self,img):
		rows, cols, ch = img.shape
		ptr1 = np.float32([[87,36],[82,482],[671,14],[664,517]])
		ptr2 = np.float32([[0,0],[0,399],[503,0],[503,399]])
		M = cv2.getPerspectiveTransform(ptr1,ptr2)
		result = cv2.warpPerspective(img, M, (504,400))
		return result


	def rotate(self,img):
		M = cv2.getRotationMatrix2D((445, 279), -20, 1)
		img_rotation = cv2.warpAffine(img, M, (self.width/2,self.height/2))
		#cv2.imshow('rotate', img_rotation)
		return img_rotation

		

	def execute(self, count):
		t = 0 
		data_x = []
		data_y = []
		while(True):
			ret, frame = self.cap.read()
			if not ret:
				break
			frame = cv2.resize(frame, (self.width/2,self.height/2))
			#frame = self.rotate(frame)
			frame = self.Perspective(frame)	
			frame = cv2.circle(frame,(self.CENTER_X,self.CENTER_Y), 1, (0,0,255), -1)
			t += 1
			#print('t = %d' % t)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(frame, (5,5), 0.0)
			bimage2 = self.bgMog2.apply(blur)
			dst2, data_x, data_y = self.findObjectAndDraw(bimage2, frame, data_x, data_y, t)
			cv2.imshow('bgMog2', dst2)
			#print(self.NAME)		
			key = cv2.waitKey(1)
			if key == 27:
				break
		if(len(data_x) != 0 ):	
			self.check_hole_in(data_x, data_y)
		f.write(unicode(count))
		f.write(unicode(' '))
		#f.write(unicode('\n'))
		#f.write(unicode(data_x))
		#f.write(unicode('\n'))
		#f.write(unicode(data_y))
		#f.write(unicode('\n'))
		f.write(unicode(self.classify))
		f.write(unicode('\n'))
		#f.write(unicode('-----------------------------------------------------------------------------------------------'))
		if self.cap.isOpened():
			self.cap.release()
		cv2.destroyAllWindows()

if __name__ == '__main__':
	
	MP4 = glob.glob('/home/hyungjun/project/golf/Video/2019_01_17_1_2/*.MP4')
	MP4.sort()
	filename = "2019_01_17_1_2.txt"	
	print('===================start=====================')
	f = io.open(filename, mode = 'wt', encoding = 'utf-8')
	count = 55
	for i in MP4:
		golf = Golf(i)
		golf.execute(count)
		count += 1
	f.close()
	print('====================End======================')
  

	


