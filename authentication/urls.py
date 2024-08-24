from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
  path("rol/list/", RoleListView.as_view()),
  path("rol/create/", RoleCreateView.as_view()),
  path("rol/update/<int:pk>/", RoleUpdateView.as_view()),
  path("rol/delete/<int:pk>/", RolDeleteView.as_view()),
    
  #Vistar para el User
  path("user/list/", UserListView.as_view()),
  path("user/create/", UserCreateView.as_view()),
  path("user/update/<int:pk>", UserUpdateView.as_view()),
  path("user/delete/<int:pk>", UserDeleteView.as_view()),
  
  # Ruta login de jwt simple
  # path("auth/login/", TokenObtainPairView.as_view()),
  
  #Ruta personalizada para el login 
  path("login/", LoginView.as_view()),
  path("refresh/", TokenRefreshView.as_view())
  
]
