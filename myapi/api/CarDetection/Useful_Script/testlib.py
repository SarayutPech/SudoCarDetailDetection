import os

opencv_path = "C:/Users/PC/AppData/Local/Programs/Python/Python38/lib/site-packages/cv2"  # Replace with the path printed above
for root, dirs, files in os.walk(opencv_path):
    for file in files:
        if file.endswith(".dll"):
            print(os.path.join(root, file))