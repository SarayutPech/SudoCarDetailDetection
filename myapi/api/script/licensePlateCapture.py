import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
import os

def convertImage(image):
    gray =cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur,50,50)
    return canny

def enchantImage(image):
    gray =cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    # blur = cv2.GaussianBlur(gray,(5,5),0)
    # canny = cv2.Canny(blur,100,100)
    return gray

def base64_to_jpg(base64_string, output_filename="decoded.jpg"):
    image_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imwrite(output_filename, img)
    img_fixed = cv2.imread(output_filename)
    return img_fixed

def image_to_base64(image):
    """แปลง OpenCV Image เป็น Base64"""
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")

def base64licenseplateCrop(base64_string):
    base64_to_jpg(base64_string,"temp.jpg")
    img = cv2.imread("temp.jpg")
    processImage = convertImage(img)
    contourImage = processImage.copy()
    license_img = None
    contours, hairachy = cv2.findContours(contourImage,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:10]
    for contour in contours:
        p = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,0.02*p,True)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(contour)
            license_img = img[y:y+h,x:x+w]
            cv2.drawContours(img,[contour],-1,(0,255,255),1)
    license_img = enchantImage(license_img)
    # cv2.imshow("Image",license_img)
    # cv2.waitKey(0)
    os.remove("temp.jpg")
    return image_to_base64(license_img)

def licenseplateCrop(image):
    img = cv2.imread("testImage1.jpg")
    processImage = convertImage(img)
    contourImage = processImage.copy()
    contours, hairachy = cv2.findContours(contourImage,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:10]
    for contour in contours:
        p = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,0.02*p,True)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(contour)
            license_img = img[y:y+h,x:x+w]
            # cv2.drawContours(img,[contour],-1,(0,255,255),1)
    license_img = enchantImage(license_img)
    cv2.imshow("Image",license_img)
    cv2.waitKey(0)