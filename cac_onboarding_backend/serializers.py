from rest_framework import serializers
# from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterSeralizer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    
class LoginSeralizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        

        if username and password:

            user = authenticate(username=username, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Incorrect crediential. Please try again')
        else:
            raise serializers.ValidationError('username or password is empty')
        
        return user
    


# class UserSerializer(serializers.ModelSerializer):
#     username  = serializers.CharField(max_length=200,required = True)
#     email_address = serializers.EmailField(max_length=200,required = True)
#     password = serializers.CharField(max_length=200, required=True)

#     class Meta:
#         model = User
#         fields = ('__all__') 
    
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username = validated_data['username'],
#             email_address = validated_data['email_address'],
#             password = validated_data['password']
#         )

#         return user


from .models import *
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location_Map
        fields = ['id', 'name', 'latitude', 'longitude', 'duration', 'cost']
        read_only_fields = ['cost']