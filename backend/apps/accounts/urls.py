from django.urls import path, include
from .views import CustomTokenObtainPairView, UserRegistrationView


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    # path("login/forgot-password/",),    
]
