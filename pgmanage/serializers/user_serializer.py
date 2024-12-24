from rest_framework import serializers
from pgmanage.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName', 'contact', 'adharNumber', 'adharImage', 'role', 'password',]
        extra_kwargs = {'password': {'write_only': True}}  # To ensure password is not exposed

    def create(self, validated_data):
        # Extract the adharImage from validated_data safely
        adhar_image = validated_data.pop('adharImage', None)  # Pop adharImage from data
        
        # Create the user instance
        user = User(
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            contact=validated_data['contact'],
            adharNumber=validated_data['adharNumber'],
            role=validated_data['role'],
           
            
        )

        # Save the image if provided
        if adhar_image:
            user.adharImage = adhar_image
        
        # Set password securely
        user.set_password(validated_data['password'])
        user.save()
        
        return user
