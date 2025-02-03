import subprocess
import re

def run_detect():
    # คำสั่งที่ต้องการรัน
    command = [
        "python",
        "asset\lib\yolov5\detect_single_image.py",
        "--weights", r"asset\lib\yolov5\runs\train\exp3\weights\best.pt",
        "--img", "640",
        "--conf", "0.25",
        "--source", "asset\lib\yolov5\data\images"
    ]

    try:
        # เรียกใช้งาน subprocess เพื่อรันคำสั่ง
        result = subprocess.run(command, capture_output=True, text=True)

        # แสดงผลลัพธ์ที่ได้จาก stdout
        # print("Output:")
        # print(result.stdout)

        res = result.stdout
        truckplate_match = re.search(r"TruckPlate\s*:\s*([^\n]+)", res)
        fullcar_match = re.search(r"Fullcar\s*:\s*([^\n]+)", res)

        # ตรวจสอบว่ามีการจับคู่หรือไม่
        if truckplate_match:
            truckplate = truckplate_match.group(1).strip()  # ใช้ .strip() เพื่อลบช่องว่างที่เกิน
        else:
            truckplate = None

        if fullcar_match:
            fullcar = fullcar_match.group(1).strip()
        else:
            fullcar = None

        # แสดงผลลัพธ์
        print("TruckPlate:", truckplate)
        print("Fullcar:", fullcar)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Image analyzing")
    run_detect()