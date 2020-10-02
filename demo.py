import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\Pavan Bhadaja\tesseract.exe'
from cv2 import cv2

img= cv2.imread('12.jpg')
img = cv2.resize(img,(600,400))
cv2.imshow("",img)
cv2.waitKey(0)
print(tess.image_to_string(img, timeout=5,lang="eng"))