from rest_framework import serializers
from .models import *

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','image'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
        from django.contrib.auth.hashers import make_password
        hashed_password = make_password('your_default_password')
        make_password(hashed_password)

    # def save(self, **kwargs):
    #     user = super().save(**kwargs)
        
    #     # If the user has provided an image
    #     if 'image' in self.validated_data:
    #         image = self.validated_data['image']
            
    #         # Get the user's ID
    #         user_id = user.id
            
    #         # Determine the image format (extension)
    #         if image.name.lower().endswith('.jpg') or image.name.lower().endswith('.jpeg'):
    #             image_format = 'jpg'
    #         elif image.name.lower().endswith('.png'):
    #             image_format = 'png'
    #         else:
    #             # Default to jpg if format cannot be determined
    #             image_format = 'jpg'
            
    #         # Modify the image name
    #         image_name = f"{user_id}.{image_format}"
            
    #         # Save the modified image name
    #         user.image.name = image_name
    #         user.save(update_fields=['image'])
        
    #     return user
   