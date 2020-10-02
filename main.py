from fpt import four_point_transform
from skimage.filters import threshold_local
import pytesseract
import numpy as np
from cv2 import cv2
import imutils
import sys

# image_fullpath=sys.argv[1]
# image_name=sys.argv[2]


# Image=cv2.imread(str(image_fullpath))

# image_save_path=image_fullpath.replace(image_name,"temp.png")

#--------------------

#--------------------
Image = cv2.imread('14.jpeg')

width,height,_ = Image.shape
ratio =0.25
print(width,height)
Original = Image.copy()
image = cv2.resize(Image,(int(height*ratio),int(width*ratio)))
print(image.shape)
# image_ogratio = image.copy()
# image = imutils.resize(image, height = 500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gray)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imshow("blur",gray)

# gray = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imshow("Blurred",gray)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
eqhisted = clahe.apply(gray)
# cv2.imshow("eqhisted",eqhisted)

# cv2.imshow("eqhisted",eqhisted)
# cv2.imshow("Blurred2",gray)

edged = cv2.Canny(eqhisted, 25, 100)
# cv2.imshow("edged",edged)

kernel = np.ones((5,5),np.uint8)
edged = cv2.dilate(edged,kernel,iterations = 1)

# cv2.imshow("dilate",edged)


# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
else:
	print("Approx",approx)
	screenCnt = approx[:4]
	
# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(Image, screenCnt.reshape(4, 2) / ratio)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped= cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

# cv2.drawContours(image,cnts,-1,(0,0,255),2)
# cv2.imshow("Contours",image)
# cv2.imshow("Warped",cv2.resize(warped,(int(height*ratio),int(width*ratio))))

# blur = cv2.GaussianBlur(warped,(3,3),0)
# edged = cv2.Canny(blur, 25, 100)
# cv2.imshow("edged",edged)

th3 = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_OTSU,11,2)

# ret3,th3 = cv2.threshold(warped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("thresholded",warped)
cv2.waitKey(0)
#--------------------------------
# # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
# edged = cv2.Canny(th3, 25, 100)
# # dilation = cv2.dilate(edged, rect_kernel, iterations = 8) 

# # cv2.imshow("dialeted",cv2.resize(dilation,(int(height*ratio),int(width*ratio))))

# # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 
# # for cnt in contours: 
# #     x, y, w, h = cv2.boundingRect(cnt) 
      
# #     # Drawing a rectangle on copied image 
# #     rect = cv2.rectangle(warped, (x, y), (x + w, y + h), (0, 255, 0), 2) 
# # cv2.imshow("dfg",cv2.resize(warped,(int(height*ratio),int(width*ratio))))
# #--------------------------------

# def dilate(ary, N, iterations):
#     """Dilate using an NxN '+' sign shape. ary is np.uint8."""
#     rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
#     # kernel = np.zeros((N, N), dtype=np.uint8)
#     # kernel[(N - 1) // 2, :] = 1
#     dilated_image = cv2.dilate(ary / 255, rect_kernel, iterations=iterations)

#     # kernel = np.zeros((N, N), dtype=np.uint8)
#     # kernel[:, (N - 1) // 2] = 1
#     # dilated_image = cv2.dilate(dilated_image, rect_kernel, iterations=iterations)
#     dilated_image = dilated_image.astype('uint8')
#     return dilated_image
# """Dilate the image until there are just a few connected components.
# Returns contours for these components."""
# # Perform increasingly aggressive dilation until there are just a few
# # connected components.
# count = 21
# dilation = 5
# n = 1
# while count > 16:
# 	n += 1
# 	dilated_image = dilate(edged, N=3, iterations=n)
# 	contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 	count = len(contours)
# # print dilation
# # Image.fromarray(edges).show()
# # Image.fromarray(255 * dilated_image).show()
# cv2.imshow("dialted",dilated_image)
# for cnt in contours: 
#     x, y, w, h = cv2.boundingRect(cnt) 
      
#     # Drawing a rectangle on copied image 
#     rect = cv2.rectangle(warped, (x, y), (x + w, y + h), (0, 255, 0), 2) 
# cv2.imshow("dfg",cv2.resize(warped,(int(height*ratio),int(width*ratio))))



# #---------------------------------------------------


# # cv2.imshow("Original", imutils.resize(image_ogratio, height = 650))
# # cv2.imshow("Resized",image)
# cv2.imshow("Scanned",cv2.resize(th3,(int(height*ratio),int(width*ratio))))
# cv2.waitKey(0)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Pavan Bhadaja\tesseract.exe'
# print(pytesseract.image_to_string(th3, timeout=5,lang="eng")) # Timeout after 2 seconds

# def tokenizer(txt):
#     lines = txt.split("\n")
#     tokens = []
#     for line in lines:
#         line = line.strip()
#         if len(line) > 0:
#             tokens.append(line)

#     return tokens()
