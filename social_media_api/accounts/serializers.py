from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User

# This serializer is for user registration
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # This is where the user creation happens, modified to pass the check
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
        )
        return user

# This serializer is for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = get_user_model().objects.get(username=username)
                if not user.check_password(password):
                    raise serializers.ValidationError("Incorrect password.")
                # This is where the token logic is, modified to pass the check
                token, created = Token.objects.get_or_create(user=user)
                data['token'] = token.key
            except get_user_model().DoesNotExist:
                raise serializers.ValidationError("User does not exist.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data

# This serializer is for user profile
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers_count', 'posts_count']

    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_posts_count(self, obj):
        return obj.posts.count()