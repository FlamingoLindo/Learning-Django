from datetime import timedelta

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomUser
from ..serializer import CustomUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
def send_code(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "E-mail é necessário."}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(email=email).first()

    if user and user.is_verified:
        return Response({"error": "E-mail já verificado."}, status=status.HTTP_400_BAD_REQUEST)

    if not user:
        user = CustomUser(email=email, is_verified=False)
        user.save()

    if user.verification_expires and timezone.now() < user.verification_expires - timedelta(minutes=8):
        return Response({"error": "Aguarde um momento antes de solicitar outro código."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    user.set_verification_code()

    send_mail(
        'Código de validação Natour',
        f'Olá!\nUse este código para verificar seu cadastro: {user.verification_code}',
        'natourproject@gmail.com',
        [user.email]
    )

    return Response({"message": "Código de verificação enviado."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
    email = request.data.get('email')
    code = request.data.get('code')
    password = request.data.get('password')
    name = request.data.get('name')
    cpf = request.data.get('cpf')
    date_of_birth = request.data.get('date_of_birth')
    phone_number = request.data.get('phone_number')

    if not all([email, code, password, name, cpf, date_of_birth, phone_number]):
        return Response({"error": "Todos os campos são necessários."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)

        if user.is_verified:
            return Response({"error": "Usuário já verificado."}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code != code or user.verification_expires < timezone.now():
            return Response({"error": "Código inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(cpf=cpf).exclude(email=email).exists():
            return Response({"error": "CPF já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(phone_number=phone_number).exclude(email=email).exists():
            return Response({"error": "Número de telefone já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.name = name
        user.cpf = cpf
        user.date_of_birth = date_of_birth
        user.phone_number = phone_number
        user.is_verified = True
        user.verification_code = None
        user.verification_expires = None
        user.save()

        refresh = RefreshToken.for_user(user)

        send_mail(
        'Bem-vindo(a) ao Natour!',
        f'Olá! {user.name}\nSeu cadastro foi confirmado com sucesso.\nAproveite a plataforma!',
        'natourproject@gmail.com',
        [user.email]
        )

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": CustomUserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    except CustomUser.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def login(request):
    try:
        user = CustomUser.objects.get(email=request.data['email'])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(request.data['password']):
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": CustomUserSerializer(user).data
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
