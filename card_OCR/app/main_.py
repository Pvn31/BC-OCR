from .fpt import four_point_transform
import os
import pytesseract
import numpy as np
from cv2 import cv2
from card_OCR import settings
from .Recognizer.contact import is_contact
from .Recognizer.email import is_email
from .Recognizer.pincode import is_pincode
from .Recognizer.website import is_website
from .Recognizer.states import find_best_guessed_state
from .Recognizer.cities import find_best_guessed_city
from .Recognizer.address import is_address
from .Recognizer.name import find_best_guessed_name

def downsize_image(image,max_height=620,max_width=1080):
    # max_width = 1080
    # max_height = 620
    height,width = image.shape
    scale_w = max_width/width
    scale_h = max_height/height


    if(width<=max_width):
        if(height<=max_height):
            #dont resize
            pass
        else:
            #resize height dimension
            image = cv2.resize(image,(int(width),int(height*scale_h)))
    else:
        if(height<=max_height):
            #resize width dimension
            image = cv2.resize(image,(int(width*scale_w),int(height)))
        else:
            #resize both dimension
            image = cv2.resize(image,(int(width*scale_w),int(height*scale_h)))
    
    return image,scale_h,scale_w


def preprocessor(img_path):
    image_og = cv2.imread(img_path)
    #downsize image for performance
    image_size = 1024
    orig_height, orig_width, _ = image_og.shape
    scale = orig_width / image_size

    image = cv2.resize(image_og, (image_size, int(orig_height / scale + 1)), None)
    # cv2.imshow("image",image)
    # print(image.shape,scale_h,scale_w)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray",gray)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # cv2.imshow("blur",blur)

    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # eqhisted = clahe.apply(gray)

    edged = cv2.Canny(blur, 25, 100)
    # cv2.imshow("edged",edged)
    kernel = np.ones((5,5),np.uint8)
    dialeted = cv2.dilate(edged,kernel,iterations = 1)
    # cv2.imshow("dialeted",dialeted)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts, hierarchy = cv2.findContours(dialeted, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
        print("Couldnot find contour with four points!!!")
        print("Using first four points from approx")
        screenCnt = approx[-4:]
        
    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(image_og, screenCnt.reshape(4, 2)* scale)
    # convert the warped image to grayscale, then threshold i
    # to give it that 'black and white' paper effect
    warped= cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # warped,_,_ = downsize_image(warped)
    # cv2.imshow("warped",warped)
    # th3 = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,11)
    ret3,th3 = cv2.threshold(warped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #downsize and convert to 300 dpi
    th3,scale_h,scale_w = downsize_image(th3)
    # cv2.imshow("th3",th3)
    # cv2.waitKey(0)
    return th3


def tokenizer(txt):
    lines = txt.split("\n")
    tokens = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            tokens.append(line)

    return tokens

def test(img_path):
    path = os.path.join(settings.MEDIA_ROOT, img_path)

    im = preprocessor(path)
    cv2.imshow("im",im)
    cv2.waitKey(0)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Pavan Bhadaja\tesseract.exe'
    txt = pytesseract.image_to_string(im, timeout=5,lang="eng") # Timeout after 5 seconds
    tokens = tokenizer(txt)
    # print(txt)
    print(tokens)
    # print(find_best_guessed_city(tokens))
    city=find_best_guessed_city(tokens)

    # print(find_best_guessed_state(tokens))
    state=find_best_guessed_state(tokens)
    # # print(find_best_guessed_name(tokens))
    name=find_best_guessed_name(tokens)
    # print(is_address(tokens))
    address=is_address(tokens)
    contacts=[]
    pincode=[]
    email=[]
    website=[]
    for token in tokens:
        # print(token)
        c = is_contact(token)
        if(len(c)):
            contacts.extend(c)
        # print(contacts)
        if(not len(contacts)):
            # print(is_pincode(token))
            p=is_pincode(token)
            if(len(p)):
                pincode.extend(p)
        # print(is_email(token))
        e=is_email(token)
        if(len(e)):
            email.extend(e)
        # print(is_website(token))
        w=is_website(token)
        if(len(w)):
            website.extend(w)
    return contacts,pincode,email,website,city,state,address,name

# for filename in enumerate(os.listdir("D:\SEM-7\Project\Data_Extraction\BC_OCR\Imgs")): 
#     print(filename)
#     src ='D:\SEM-7\Project\Data_Extraction\BC_OCR\Imgs\\'+ filename[1]
#     im = preprocessor(src)
#     # cv2.imshow("im",im)
#     # cv2.waitKey(0)
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Pavan Bhadaja\tesseract.exe'
#     txt = pytesseract.image_to_string(im, timeout=5,lang="eng") # Timeout after 5 seconds
#     tokens = tokenizer(txt)
#     print("raw txt =>",txt)
#     print("tokens =>",tokens)
#     city = find_best_guessed_city(tokens)
#     state = find_best_guessed_state(tokens)
#     name = find_best_guessed_name(tokens)
#     address = is_address(tokens)
#     contact = []
#     pincode = []
#     email = []
#     website = []
#     for token in tokens:
#         # print(token)
#         contacts = is_contact(token)
#         if(len(contacts)):
#             contact.extend(contacts)
#         if(not len(contacts)):
#             p = is_pincode(token)
#             if(len(p)):
#                 pincode.extend(p)
#         e = is_email(token)
#         if(len(e)):
#             email.extend(e)
#         w = is_website(token)
#         if(len(w)):
#             website.extend(w)
#     print('-'*45)
#     print("name : ",name)
#     print("email : ",email)
#     print("contact : ",contact)
#     print("pincode : ",pincode)
#     print("Address : ",address)
#     print("City : ",city)
#     print("State : ",state)
#     print("Website : ",website)