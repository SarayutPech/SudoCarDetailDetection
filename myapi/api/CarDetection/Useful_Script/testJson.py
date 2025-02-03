import json
import sys

def main():
    # ตัวอย่างข้อมูลที่ต้องการส่งกลับ
    result = {
        "status": "success",
        "detections": [
            {"label": "person", "confidence": 0.87, "box": [50, 30, 200, 400]},
            {"label": "car", "confidence": 0.93, "box": [300, 150, 500, 400]},
        ]
    }

    # แปลงข้อมูลเป็น JSON และพิมพ์ออกทาง stdout
    print(json.dumps(result))

if __name__ == "__main__":
    main()
