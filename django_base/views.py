from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class HelloWorldView(APIView):
    def get(self, request):
        if 'name' in request.query_params:
            return Response({'message': 'Hello, ' + request.query_params['name'] + '!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Hello, world!'}, status=status.HTTP_200_OK)
    
    def post(self, request):
        if 'name' in request.data:
            return Response({'message': 'Hello, ' + request.data['name'] + '!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Hello, world in post!'}, status=status.HTTP_200_OK)