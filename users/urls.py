from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView
from .views import ResetPasswordView, ResetPasswordConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
    path('reset-password-confirm/<str:token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),

]
