from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

# Esto lo que vamos hacer es una personalizacion de permisos para nuestra Autenticacion , en ves de usar IsAuthenticated , personalizamos la nuestra

# Esto controla que el usuario este autenticado
class IsAutenticado(BasePermission):  
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      raise AuthenticationFailed(detail={
        "message": "Unauthorized"
      }, code=401)
    
    return True

class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    # print(request.user) => Esto me devuelve el gmail del usuario autenticado 
    # print(request.user.is_authenticated) => Devuelve un True o False si esque el usuario esta autenticado o no
    # print(request.user.role_id.name) => Te imprime que rol tiene el usuario , si es ADMIN o CLIENT
    
    if request.user.role_id.name != "ADMIN":
      raise AuthenticationFailed(detail={
        "message": "Unauthorized"
      }, code=401)

    return True

class IsClient(BasePermission):
  def has_permission(self, request, view):
    if request.user.role_id.name != "CLIENT":
      raise AuthenticationFailed(detail={
        "message": "Unauthorized"
      }, code=401)

    return True