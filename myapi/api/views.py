from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .CarDetection.asset.lib.yolov5.detectSingleImage import run
    
class GetLicensePlate(APIView):
    def post(self, request):
        data = request.data
        if "image" not in data:
            return Response(
                data={"status": "error", "code": 400, "message": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        print("data image : " , data["image"][:100] , "...")
        base64_input_images = [
        data["image"]
        ]
        detechedObject = run(weights="model.pt", base64_images=base64_input_images)

        return Response(
            data={"data": detechedObject,"status": "Success", "code": 200, "message": "Success"},
            status=status.HTTP_200_OK
        )