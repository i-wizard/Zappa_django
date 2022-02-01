from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import User
from .serializers import *
from utils.rate_limiter import UserLoginLimiter

class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message":"User created successfully, procceed to login.", "status":True}, status=status.HTTP_201_CREATED)
    
@throttle_classes([UserLoginLimiter])
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        user = User.objects.get(username=username)
        tokens = user.get_tokens()
        user_data = UserSerializer(user).data
        return Response(data={"message":"Login successful", "status":True, "data":{**user_data, **tokens}}, status=status.HTTP_200_OK)
    
