from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk})

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if current_user == target_user:
        return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    current_user.following.add(target_user)
    return Response({"message": f"You are now following {target_user.username}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    if current_user == target_user:
        return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    current_user.following.remove(target_user)
    return Response({"message": f"You have unfollowed {target_user.username}"}, status=status.HTTP_200_OK)
