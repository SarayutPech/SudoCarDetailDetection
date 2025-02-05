from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .CarDetection.asset.lib.yolov5.detectSingleImageWindow import run
from .CarDetection.asset.lib.tesseract_ocr.ocr import extractNumbersFromBase64
from .CarDetection.Useful_Script.ImageProcessing import *
from .script.licensePlateCapture import base64licenseplateCrop

    
class GetLicensePlate(APIView):
    def post(self, request):
        res = {
                "plateNo":None,
                "brand":None
            }
        try:
            data = request.data
            if "image" not in data:
                return Response(
                    data={"status": "error", "code": 400, "message": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # print("data image : " , data["image"][:100] , "...")
            
            base64_input_images = [
            data["image"]
            ]
            detechedObject = run(weights="model.pt", base64_images=base64_input_images)
            # detechedObject["results"][0]["TruckPlate"] = base64licenseplateCrop(detechedObject["results"][0]["TruckPlate"])
            # detechedObject["results"][0]["TruckPlate"] = sharpen_image(detechedObject["results"][0]["TruckPlate"])
            number = extractNumbersFromBase64(detechedObject["results"][0]["TruckPlate"])
            print(number)
            res["plateNo"] = number[0] + "-" + number[1]

            return Response(
                data={"detail":res,
                    #   "data": detechedObject,
                      "status": "Success", "code": 200, "message": "Success"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"detail":res,
                    #   "data": detechedObject,
                      "status": "Internal Server Error", "code": 500, "message": "Internal Server Error"},
                status=500
            )