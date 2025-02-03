import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# ฟังก์ชันสำหรับการโหลดและเตรียมรูปภาพ
def preprocess_image(image_path, input_size=(640, 640)):
    # โหลดภาพและแปลงเป็น RGB
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Resize ภาพให้เป็น 640x640
    image_resized = cv2.resize(image, input_size)
    # Normalize ค่าระหว่าง 0-1
    image_normalized = image_resized / 255.0
    # เพิ่มมิติให้เป็น (1, 640, 640, 3)
    image_input = np.expand_dims(image_normalized, axis=0).astype('float32')
    # ทำซ้ำภาพเดิมสามครั้งให้เป็น (3, 640, 640, 3)
    image_input = np.tile(image_input, (3, 1, 1, 1))
    return image, image_input  # คืนค่า image แบบดั้งเดิมและ image ที่เตรียมพร้อมสำหรับโมเดล

# โหลดโมเดล TFLite
interpreter = tf.lite.Interpreter(model_path="best-fp16.tflite")
interpreter.allocate_tensors()

# ดึงข้อมูลเกี่ยวกับ input และ output ของโมเดล
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ตรวจสอบขนาดที่โมเดลคาดหวัง
input_shape = input_details[0]['shape']
print("Input shape adjusted to:", input_shape)

# เตรียมภาพสำหรับทำการพยากรณ์
image_path = "car_2.jpg"  # เปลี่ยนเป็นพาธของภาพที่ต้องการทดสอบ
original_image, input_data = preprocess_image(image_path, (640, 640))

# ใส่ข้อมูลภาพเข้าไปในโมเดล
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# ดึงผลลัพธ์จากโมเดล
output_data = interpreter.get_tensor(output_details[0]['index'])

# วาด bounding boxes บนภาพตามข้อมูลที่ได้ (ใช้ผลลัพธ์เฉพาะจาก batch แรกเท่านั้น)
for detection in output_data[0]:
    if len(detection) >= 6:
        x_min, y_min, x_max, y_max, confidence, class_id = detection[:6]
        if confidence > 0.1:
            x_min = int(x_min * original_image.shape[1])
            y_min = int(y_min * original_image.shape[0])
            x_max = int(x_max * original_image.shape[1])
            y_max = int(y_max * original_image.shape[0])
            cv2.rectangle(original_image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            label = f'Class: {int(class_id)}, Conf: {confidence:.2f}'
            cv2.putText(original_image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# แสดงภาพพร้อม bounding boxes
plt.imshow(original_image)
plt.axis('off')
plt.show()
