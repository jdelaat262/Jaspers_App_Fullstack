from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Deelnemer
from .serializers import DeelnemerSerializer

class DeelnemerAPIView(APIView):
    def post(self, request):
        # Hier gebruik je de DeelnemerSerializer, die weer gebruik maakt van het Deelnemer-model
        serializer = DeelnemerSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ping_view(request):
    return Response({'message': 'Hello world, de backend is verbonden!'})
