import os
from PIL import Image
import shutil
import re

# เอาไฟล์รูปไปไว้ใน ./Asset/Image/CarImageCollection 
# โดย format มักจะเป็น ./Asset/Image/CarImageCollection/วันที่/ชั่วโมง/ไฟล์รูป.jpg

# Variable 
car_image_count = 0
result_directory = "./Asset/Image/FullCarImage"
result_image_directory = "./Asset/Image/FullCarImage/car_"
image_directory = "./Asset/Image/CarImageCollection" 

def list_folders_in_current_dir(directory):
    folders = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            folders.append(item)
    return folders

def count_images_with_size(root_folder, target_folder, width=2448, height=2048):
    global car_image_count
    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    if img.size == (width, height):
                        car_image_count += 1
                        # print("copy full car image. " + str(car_image_count))
                        shutil.copy(file_path, target_folder + str(car_image_count) +".jpg")
                    # else:
                        # print("pattern not like full car image.")
            except Exception:
                # Ignore files that are not images or cannot be opened
                pass
    return car_image_count

def get_max_car_number(directory):
    max_number = -1  # เริ่มต้นที่ -1 เพราะหมายเลขไม่สามารถต่ำกว่านี้ได้
    pattern = r"car_(\d+)"  # รูปแบบที่ต้องการค้นหา (car_xxx)

    for filename in os.listdir(directory):
        match = re.match(pattern, filename)  # ตรวจสอบว่าชื่อไฟล์ตรงตามรูปแบบที่กำหนดหรือไม่
        if match:
            number = int(match.group(1))  # แปลงตัวเลขที่ค้นพบให้เป็น int
            if number > max_number:
                max_number = number  # อัปเดต max_number ถ้าตัวเลขใหม่มากกว่า

    return max_number


folders = list_folders_in_current_dir(image_directory)
try:
    car_image_count = get_max_car_number(result_directory)
except:
    car_image_count = 0
print("================= Current Car Image =================")
print(f"New car image start at {car_image_count}")
print("================= View All Folders =================")
print("Current working directory:", os.getcwd())
for folder in folders:
    sub_directory = image_directory + "/" + folder
    sub_folders = list_folders_in_current_dir(sub_directory)
    print("-> " + sub_directory)
    for sub_folder in sub_folders:
        image_count = count_images_with_size(sub_directory+"/"+sub_folder
                                             ,result_image_directory)
print("-> car_image_download_size : " + str(car_image_count))



