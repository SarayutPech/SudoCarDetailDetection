from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .CarDetection.asset.lib.yolov5.detectSingleImageWindow import run
from .CarDetection.asset.lib.tesseract_ocr.ocr import extractNumbersFromBase64
from .CarDetection.Useful_Script.ImageProcessing import *
from .script.licensePlateCapture import base64licenseplateCrop
from .CarDetection.Useful_Script.Load_Image_To_Dir import runScript as LoadImageToDirRunScript


class LoadImageSet(APIView):
    def post(self, request):
        try:
            LoadImageToDirRunScript("./dataForTrain/rawImage","./dataForTrain/fullImage")
            return Response(
                data={
                      "status": "Success", "code": 200, "message": "Success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={
                      "status": "Internal Server Error", "code": 500, "message": "Internal Server Error"},
                status=500
            )

class resizeImageSet(APIView):
    def post(self, request):
        try:
            runScript("./dataForTrain/rawImage","./dataForTrain/fullImage")
            return Response(
                data={
                      "status": "Success", "code": 200, "message": "Success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={
                      "status": "Internal Server Error", "code": 500, "message": "Internal Server Error"},
                status=500
            )

class GetBlurImage(APIView):
    def post(self, request):
        res = {
                "blurImage":None
            }
        try:

            return Response(
                data={"detail":res,
                      "status": "Success", "code": 200, "message": "Success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"detail":res,
                      "status": "Internal Server Error", "code": 500, "message": "Internal Server Error"},
                status=500
            )
    
class GetLicensePlate(APIView):
    def post(self, request):
        res = {
                "plateNo":None
                # ,"brand":None
            }
        try:
            data = request.data
            if "image" not in data:
                return Response(
                    data={"status": "error", "code": 400, "message": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            base64_input_images = [
            data["image"]
            ]
            detechedObject = run(weights="model.pt", base64_images=base64_input_images)
            number = extractNumbersFromBase64(detechedObject["results"][0]["TruckPlate"])
            print(number)
            res["plateNo"] = number[0] + "-" + number[1]

            return Response(
                data={"detail":res,
                      "status": "Success", "code": 200, "message": "Success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"detail":res,
                      "status": "Internal Server Error", "code": 500, "message": "Internal Server Error"},
                status=500
            )