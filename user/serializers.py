from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from utils.helper import Helper


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration.
    Rules:
        username can only be one word, any space will be stripped off
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop("username")
        try:
            username = Helper.clean_username(username)
        except Exception as e:
            raise serializers.ValidationError(e.args)
        if User.objects.filter(email__iexact=validated_data.get("email")).exists():
            raise serializers.ValidationError(
                "User with this email already exist")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "User with this username already exist")
        user = User.objects.create_user(**validated_data, username=username)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Password and username are case sensitive"
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            raise AuthenticationFailed("Username or password incorrect!")
        if not user.is_active:
            raise AuthenticationFailed(
                "This account has been blocked, contact support!")
        print('user', user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
