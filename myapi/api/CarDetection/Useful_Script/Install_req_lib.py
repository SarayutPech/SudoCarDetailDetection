import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./Asset/Lib/yolov5-master/requirements.txt"])
        print("Libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while installing libraries:", e)

if __name__ == "__main__":
    install_requirements()