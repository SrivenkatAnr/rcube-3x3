import numpy as np
try:
	import cv2
except:
	import cv2
from core.cube_feature import featureExtract

side0 = cv2.imread("images/solved/image1.jpeg")
side1 = cv2.imread("images/solved/image2.jpeg")
side2 = cv2.imread("images/solved/image3.jpeg")
side3 = cv2.imread("images/solved/image4.jpeg")
side4 = cv2.imread("images/solved/image5.jpeg")
side5 = cv2.imread("images/solved/image6.jpeg")

cube_ext = featureExtract([side0,side1,side2,side3,side4,side5])

sides = cube_ext.grid

i=0
for side in sides:
	np.savetxt("temp/side{}.txt".format(i),side)
	i+=1

