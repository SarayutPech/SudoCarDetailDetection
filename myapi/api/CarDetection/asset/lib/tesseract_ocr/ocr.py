import easyocr
import base64
import re
from PIL import Image
import io
import numpy as np

def extractNumbersFromBase64(base64_string):
    """ใช้ OCR อ่านตัวเลขจาก Base64 และแทนที่ l, I, | ด้วย 1"""
    try:
        # แปลง Base64 เป็นไบต์
        image_data = base64.b64decode(base64_string)
        
        # เปิดรูปภาพด้วย PIL แล้วแปลงเป็น NumPy array
        image = Image.open(io.BytesIO(image_data))
        image_np = np.array(image)

        # โหลดโมเดล EasyOCR (ไทย + อังกฤษ)
        reader = easyocr.Reader(['th', 'en'])

        # ใช้ OCR อ่านข้อความจากภาพ
        text_detected = reader.readtext(image_np, detail=0)

        # รวมข้อความที่ OCR ตรวจพบ
        text = ' '.join(text_detected)

        # แทนที่ตัวอักษรที่คล้ายเลข 1 ด้วย "1"
        text = text.replace('|', '1').replace('I', '1').replace('l', '1')

        # ใช้ Regular Expression ดึงเฉพาะตัวเลข
        numbers = re.findall(r'\d+', text)

        return numbers

    except base64.binascii.Error:
        return "Base64 ไม่ถูกต้อง"
    except IOError:
        return "ไม่สามารถเปิดรูปภาพจาก Base64 ได้"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

# ตัวอย่าง Base64 (ใส่ค่าจริงของ Base64 แทน)
# base64_image = "ใส่ค่ารูปภาพ Base64 ที่นี่"

# # อ่านตัวเลขจากภาพ
# numbers_detected = extractNumbersFromBase64(base64_image)
# print(numbers_detected)
