import os
from PIL import Image

# กำหนด path ของโฟลเดอร์ภาพและโฟลเดอร์ output
# image_folder = "./Model_Training_Ground/test_data/images"  # โฟลเดอร์ที่เก็บภาพต้นฉบับ
# output_image_folder = "./Model_Training_Ground/test_data/resizeImages"  # โฟลเดอร์บันทึกภาพที่ resize แล้ว

def runScript(image_folder,output_image_folder):
    os.makedirs(output_image_folder, exist_ok=True)
    new_size = (640, 640)
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # ตรวจสอบว่าเป็นไฟล์ภาพ
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path).convert("L")  # แปลงเป็น Grayscale
            image_resized = image.resize(new_size)
            output_image_path = os.path.join(output_image_folder, filename)
            image_resized.save(output_image_path)
            print(f"Processed {filename} -> Converted to grayscale & resized")
    print("✅ Resize images to grayscale completed successfully.")
