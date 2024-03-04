

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
from django.core.mail import send_mail
import random
import string
from .serializers import UserProfileUpdateSerializer, UserSerializer

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
def get_all_users(request):
    users = User.objects.filter()
    serialized_users = []

    for user in users:
        serializer = UserSerializer(user)

      
        user_data = serializer.data
        serialized_users.append(user_data)
       

    return Response(serialized_users)

@api_view(['POST'])
def verify_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = True
    user.save()

    return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE']) 
def user_profile(request, pk):
    try:
        user = User.objects.get(id=pk)
       
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        if user.image:  # Check if the image field is not empty
             image_path = user.image.path
             if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                       encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                       user_data = serializer.data
                       user_data['image'] = f"data:image/jpeg;base64,{encoded_image}"
                return Response(user_data)
             else:
                 return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user_data = serializer.data
            return Response(user_data)
        

    elif request.method == 'PUT':
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.image: 
                if 'image' in request.data:
                   old_image_path = user.image.path
                   if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                 
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'DELETE':
        image_path = user.image.path
        if os.path.exists(image_path):
            os.remove(image_path)  # Delete the image file
        user.delete()  # Delete the user
        return Response(status=status.HTTP_204_NO_CONTENT)


   




    
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
    mutable_data = request.data.copy()
    mutable_data['password'] = hashed_password


    print(hashed_password)

    serializer = UserSerializer(data=mutable_data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def send_new_password(email, new_password):
    message = f'Your new password is: {new_password}'
    send_mail('New Password', message, 'ramiferchichi32@gmail.com', [email])



@api_view(['POST'])
def verify_and_reset_password(request):
    if request.method == 'POST':
        email = request.data["email"]
        username = request.data["username"]
        print(email,username)
        if not email or not username:
            return Response({'message': 'Email and username are required.'}, status=400)

        try:
            user = User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            return Response({'message': 'Invalid email or username.'}, status=400)

        new_password = generate_password()
        user.set_password(new_password)
        user.save()
        send_new_password(email, new_password)

        return Response({'message': 'New password sent successfully.'}, status=200)

    return Response({'message': 'Method not allowed.'}, status=405)








