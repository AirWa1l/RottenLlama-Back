from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResetPasswordSerializer, ChangePasswordSerializer


User = get_user_model()

# User registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(email=response.data['email'])  # Optimización: obtenemos el usuario directamente
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#Reset password view
User = get_user_model()

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.send_reset_email(request)
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para confirmar el restablecimiento de contraseña
class ResetPasswordConfirmView(APIView):
    def post(self, request, token):
        # Verificar si el token es válido
        try:
            user = User.objects.get(reset_password_token=token)
        except User.DoesNotExist:
            return Response({"detail": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar la nueva contraseña
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Actualizar la contraseña del usuario
            user.set_password(serializer.validated_data['password'])
            user.reset_password_token = ''  # Limpiar el token de restablecimiento
            user.save()
            return Response({"detail": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)