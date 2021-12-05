from rest_framework.response import Response
from rest_framework.views import APIView



class HomeAPIView(APIView):
    def get(self, request):
        return Response({'message': 'hello user!!'})
