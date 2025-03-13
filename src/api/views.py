import time
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from accounts.decorators import extend_token


class LatencyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_token
    def get(self, request):
        url = "https://ya.ru"
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = time.time() - start
            return Response({"latency": latency})
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=500)
