from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser, Point
from .serializer import CustomUserSerializer, PointSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        serializer = CustomUserSerializer(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = CustomUser.objects.get(email=request.data['email'])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(request.data['password']):
        refresh = RefreshToken.for_user(user)
        serializer = CustomUserSerializer(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
POINTS
"""
@api_view(['POST'])
def create_point(request):
    serializer = PointSerializer(data=request.data)
    if serializer.is_valid():
        point = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_points(request):
    points = Point.objects.all()
    serializer = PointSerializer(points, many=True)
    return Response(serializer.data)