

import base64
import io
import tempfile
import time
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import json
from datetime import datetime

from .serializers import UserSerializer

import os

class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user.email),  # django.contrib.auth.User instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


@api_view(['GET'])
def user_profile(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)

        image_path = user.image.path
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                user_data = serializer.data
                user_data['image'] = f"data:image/jpeg;base64,{encoded_image}"
                return Response(user_data)
        else:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)





    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = datetime.now()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({   
            'token': token.key,
            'username':user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_id': user.pk,
            'email': user.email,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff

        })





@api_view(['POST'])
def signup(request):
    hashed_password = make_password(request.data["password"])
    print(hashed_password)
    request.data["password"] = hashed_password
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



















