import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r'asset\lib\tesseract_ocr\tesseract.exe'  
image_path = 'asset/lib/yolov5/runs/detect/exp2/crops/TruckPlate/car_292_TruckPlate_1030_1050.jpg'  

# try:
#     img = Image.open(image_path)  
#     img.show() #print image
# except FileNotFoundError:
#     print(f"ไม่พบรูปภาพ: {image_path}")

image = cv2.imread(image_path)

# แปลงภาพเป็นขาวดำเพื่อเพิ่มประสิทธิภาพ OCR
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ใช้ Adaptive Threshold เพื่อเพิ่ม contrast
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# เพิ่มความคมชัด
sharpen_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
sharpen = cv2.filter2D(thresh, -1, sharpen_kernel)

cv2.imshow('a',sharpen)

# OCR พร้อมปรับแต่งภาษาและการตั้งค่า
custom_config = r'--psm 7 --oem 3'
text = pytesseract.image_to_string(sharpen, config=custom_config, lang="eng+tha")

print("res : " + text)