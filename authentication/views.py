from rest_framework import generics, status
from rest_framework.request import Request
from .serializer import * 
from .models import *
from rest_framework.response import Response
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView

class RoleListView(generics.ListAPIView):
  queryset = RolModel.objects.all()
  serializer_class = RolSerializer
  
  def list(self, request):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    data = serializer.data 
    
    return Response({
      "message": "Roles obtenidos correctamente",
      "data": data
    }, status=status.HTTP_200_OK)
  
class RoleCreateView(generics.CreateAPIView):
  serializer_class = RolSerializer
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Rol creado correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
    
class RoleUpdateView(generics.UpdateAPIView):
  queryset = RolModel.objects.all()
  serializer_class = RolSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      return Response({
        "message": "Rol actualizado correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
    except Http404: 
      return Response({
        "message": "Rol no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
        
class RolDeleteView(generics.DestroyAPIView):
  queryset = RolModel.objects.all()
    
  def destroy(self, request, *args, **kwargs):
    try:
      super().destroy(request, *args, **kwargs)
      
      return Response({
        "message": "Rol eliminado correctamente"
      }, status=status.HTTP_204_NO_CONTENT)
    except Http404:
      return Response({
        "message": "Rol no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
  
  
# VISTAR PARA USUARIOS

class UserListView(generics.ListAPIView):
  queryset = MyUserModel.objects.all()
  serializer_class = UserSerializer

  def list(self, request):
    queryset =  self.get_queryset()
    serializer = self.get_serializer(queryset , many=True)
    data = serializer.data 
    
    return Response({
      "message": "Usuarios obtenidos correctamente",
      "data": data
    }, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
  serializer_class = UserSerializer
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Usuario creado correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
    

class UserUpdateView(generics.UpdateAPIView):
  queryset = MyUserModel.objects.all()
  serializer_class = UserSerializer
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Usuario actualizado correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
    except Http404 :
      return Response({
        "message": "Usuario no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
      
class UserDeleteView(generics.DestroyAPIView):
  queryset = MyUserModel.objects.all()
  serializer_class = UserSerializer
  
  #Siempre aplicaremos esta logica cuando queramos cambiar el status de algo
  #En este caso no estaremos eliminando el usuario porque afectaria , solo cambiaremos en status
  def destroy(self, request, *args, **kwargs):
    try:
      # Aca recuperamos la instancia y la recuperamos con get_object()
      instance = self.get_object()
      instance.status = False
      instance.save()
      
      # Haciendo esto podemos acceder a la data para que se muestre al ejecutar el metodo , ojo esto es mejor hacerlo porque si pones el super(). va a eliminarlo y solo queremos que cambie el status
      serializer = self.get_serializer(instance)  
    
      return Response({
        "message": "Usuario eliminado correctamente",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
    
    except Http404:
      return Response({
        "message": "Usuario no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
    
    
# ¿QUE ES UNA INSTANCIA? => Una instancia es una fila completa de una tabla en la base de datos, donde cada columna representa un campo definido en el modelo del archivo models.py. Cuando recuperas una instancia de una tabla, obtienes los valores específicos de esa fila para cada columna. Por ejemplo, si tienes una tabla User con columnas como phone y email, al recuperar una instancia de esa tabla, obtendrás los valores específicos de phone y email para esa fila en particular. Si pones user.phone te traera el valor de phone de esa instancia, y si pones user.email te traera el valor de email de esa instancia.

class LoginView(TokenObtainPairView):
  serializer_class = LoginSerializer
  
  # Esto solo es para que muestre un mensaje en lugar del por defecto , ese mensaje se mostrara cuando el status del usuario este en false y no pueda loguearse . Saldra el error cuando el def validate de serializer de en else
  def post(self, request: Request, *args, **kwargs):
    try:
      return super().post(request, *args, **kwargs) 
    except ValidationError as e:
      return Response({
        "message": "Unauthorized"
      }, status=status.HTTP_401_UNAUTHORIZED)

