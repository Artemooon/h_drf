from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer


class RegisterUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)