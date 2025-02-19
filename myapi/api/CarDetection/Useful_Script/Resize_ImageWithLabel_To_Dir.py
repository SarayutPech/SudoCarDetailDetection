import os
from PIL import Image

# กำหนด path ของโฟลเดอร์ภาพและโฟลเดอร์ label
image_folder = "./Model_Training_Ground/test_data/images"  # เปลี่ยนเป็น path ของโฟลเดอร์ที่เก็บภาพ
label_folder = "./Model_Training_Ground/test_data/labels"  # เปลี่ยนเป็น path ของโฟลเดอร์ที่เก็บ label
output_image_folder = "./Model_Training_Ground/test_data/resizeImages"  # โฟลเดอร์ที่ต้องการบันทึกภาพที่ resize แล้ว
output_label_folder = "./Model_Training_Ground/test_data/resizeLabels"  # โฟลเดอร์ที่ต้องการบันทึก label ที่ปรับสัดส่วนแล้ว

# สร้างโฟลเดอร์ output ถ้ายังไม่มี
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# ขนาดใหม่ที่ต้องการ
new_size = (640, 640)

# Loop ผ่านทุกไฟล์ในโฟลเดอร์
for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # ตรวจสอบว่าเป็นไฟล์ภาพ
        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt"))
        
        # เช็คว่าไฟล์ label มีอยู่จริง
        if not os.path.exists(label_path):
            print(f"Label file for {filename} not found, skipping.")
            continue
        
        # โหลดและ resize ภาพ
        image = Image.open(image_path)
        original_size = image.size
        image_resized = image.resize(new_size)
        output_image_path = os.path.join(output_image_folder, filename)
        image_resized.save(output_image_path)  # บันทึกภาพใหม่

        # อ่านและปรับ label
        with open(label_path, "r") as f:
            labels = f.readlines()

        new_labels = []
        for label in labels:
            class_id, x_center, y_center, width, height = map(float, label.split())
            
            # ปรับสัดส่วน x, y, width, height ตามขนาดใหม่
            x_center *= new_size[0] / original_size[0]
            y_center *= new_size[1] / original_size[1]
            width *= new_size[0] / original_size[0]
            height *= new_size[1] / original_size[1]
            
            # เพิ่ม label ใหม่ลงใน list
            new_labels.append(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        # เขียน label ใหม่ลงในไฟล์
        output_label_path = os.path.join(output_label_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt"))
        with open(output_label_path, "w") as f:
            f.writelines(new_labels)

        print(f"Processed {filename}")

print("Resize images and adjust labels success.")
