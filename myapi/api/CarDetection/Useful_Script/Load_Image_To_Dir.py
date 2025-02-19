import os
from PIL import Image
import shutil
import re
import datetime

# เอาไฟล์รูปไปไว้ใน ./Asset/Image/CarImageCollection 
# โดย format มักจะเป็น ./Asset/Image/CarImageCollection/วันที่/ชั่วโมง/ไฟล์รูป.jpg

# Variable 
car_image_count = 0
result_directory = "./Asset/Image/FullCarImage"
result_image_directory = "./Asset/Image/FullCarImage/car_"
image_directory = "./Asset/Image/CarImageCollection" 

def list_folders_in_current_dir(directory):
    folders = []
    try:
        if not os.path.exists(directory):
            print(f"Directory does not exist: {directory}")
            return []

        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                folders.append(item)
        
        print(f"Found {len(folders)} folders in {directory}")
    except Exception as e:
        print(f"Error while listing folders in {directory}: {e}")
    
    print("========== list_folders_in_current_dir ended ==========")
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
                        print("copy full car image. " + str(car_image_count))
                        shutil.copy(file_path, target_folder + str(car_image_count) +".jpg")
                    else:
                        print("pattern not like full car image.")
            except Exception:
                # Ignore files that are not images or cannot be opened
                pass
    print("========== count_images_with_size ==========")
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


def get_latest_dataset_number(resDir):
    """ ตรวจสอบ dataset ที่มีอยู่ แล้วคืนค่า datasetX+1"""
    existing_datasets = []
    
    if os.path.exists(resDir):
        for folder in os.listdir(resDir):
            if os.path.isdir(os.path.join(resDir, folder)) and folder.startswith("dataset"):
                try:
                    number_part = folder.split('-')[0].replace("dataset", "")
                    existing_datasets.append(int(number_part))
                except ValueError:
                    continue
    
    next_number = max(existing_datasets, default=0) + 1
    return f"dataset{next_number}"

def runScript(imgDir, resDir):
    folders = list_folders_in_current_dir(imgDir)
    
    try:
        car_image_count = get_max_car_number(resDir)
    except:
        car_image_count = 0

    print("================= Current Car Image =================")
    print(f"New car image start at {car_image_count}")
    
    print("================= View All Folders =================")
    print("Current working directory:", os.getcwd())


    # ตรวจสอบ dataset folders และสร้างชื่อใหม่
    dataset_name = get_latest_dataset_number(resDir)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_dataset_folder = f"{dataset_name}-{today_date}"
    new_dataset_path = os.path.join(resDir, new_dataset_folder)

    if not os.path.exists(new_dataset_path):
        os.makedirs(new_dataset_path)
        print(f"Created new dataset folder: {new_dataset_path}")
    else:
        print(f"Dataset folder already exists: {new_dataset_path}")

    for folder in folders:
        sub_directory = os.path.join(imgDir, folder)
        sub_folders = list_folders_in_current_dir(sub_directory)
        for sub_folder in sub_folders:
            sub_path = os.path.join(sub_directory, sub_folder)
            print("sub_directory:", sub_path)
            image_count = count_images_with_size(sub_path, new_dataset_path + "/car_")
    
    print("-> car_image_download_size:", car_image_count)

    



