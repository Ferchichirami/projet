from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


        from django.contrib.auth.hashers import make_password
        hashed_password = make_password('your_default_password')
        make_password(hashed_password)