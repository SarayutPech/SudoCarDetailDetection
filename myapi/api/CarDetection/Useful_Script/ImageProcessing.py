import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image


def base64_to_image(base64_string):
    """ แปลง Base64 เป็น OpenCV Image """
    img_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def image_to_base64(image):
    """ แปลง OpenCV Image เป็น Base64 """
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def sharpen_image(base64_input):
    """ เพิ่มความคมชัดให้ภาพ """
    image = base64_to_image(base64_input)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, sharpen_kernel)
    return image_to_base64(sharpened)

def super_resolution_espcn(base64_input, model_path="ESPCN_x4.pb"):
    """ ใช้ ESPCN เพิ่มความละเอียดของภาพ """
    image = base64_to_image(base64_input)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("espcn", 4)
    upscaled = sr.upsample(image)
    return image_to_base64(upscaled)

