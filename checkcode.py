#-*-encoding:utf-8-*-
"""
author: sixseven
date: 2018-05-16
topic: 使用opencv进行验证码识别
contact: 2557692481@qq.com
"""
import cv2
import numpy as np

# 两张图片的相似程度
def mse(image1,image2):
	err = np.sum((image1.astype(float)-image2.astype(float))**2)
	err /= float(image1.shape[0]*image1.shape[1])
	return err

# 切割后的验证码最接近什么数字/字母
def compare(image):
	count = 999999
	result = 0
	for i in range(0,9):
		image_com = cv2.imread('./train/{0}.jpg'.format(i))
		mse_res = mse(image,image_com)
		if mse_res < count:
			result = i
			count = mse_res
	return result

# 验证码识别
def distinguish(filename):
	# 读取图片
	image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

	# 擦除噪点和干扰线
	kernel = np.ones((1,1),np.uint8)
	erosion = cv2.erode(image,kernel,iterations=1)

	# 模糊操作
	blurred = cv2.GaussianBlur(erosion,(5,5),0)

	# 边界
	edged = cv2.Canny(blurred,30,60)

	# 膨胀
	dilation = cv2.dilate(edged,kernel,iterations=1)

	# 侦测轮廓
	image,contours,hierarchy = cv2.findContours(dilation.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted([(c,cv2.boundingRect(c)[0]) for c in contours],key=lambda x:x[1])

	arr = []
	for (c,_) in cnts:
		(x,y,w,h) = cv2.boundingRect(c)
		if w>=9 and w<=13 and h>=15 and h<=19:
			Flag = False
			for i in range(-2,3):
				for j in range(-2,3):
					for k in range(-2,3):
						for l in range(-2,3):
							if (x+i,y+j,w+k,h+l) in arr:
								Flag = True
								break
						if Flag:
							break
					if Flag:
						break
				if Flag:
					break
			if not Flag:
				arr.append((x,y,w,h))
	check_result = ''
	for item in arr:
		(x,y,w,h) = item
		img = dilation[y:y+h,x:x+w]
		res = cv2.resize(img,(12,18))
		cv2.imwrite('./split.jpg',res)
		res = cv2.imread('./split.jpg')
		check_result += str(compare(res))
	return check_result
