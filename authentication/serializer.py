from typing import Any, Dict
from rest_framework import serializers 
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authentication import authenticate
from rest_framework.serializers import ValidationError

class RolSerializer(serializers.ModelSerializer):
  class Meta:
    model = RolModel
    fields = "__all__"
    
class UserSerializer(serializers.ModelSerializer):
  #Esto sirve para que cuando listes tus usuarios , no te muestre la contraseña
  password = serializers.CharField(write_only=True)
  
  class Meta: 
    model = MyUserModel
    fields = "__all__"
    
  # OJO => Esto solo lo hacemos para encriptar la contraseña y solo se hace cuando nosotros queremos una tabla User personalizada , en este caso la personalizamos en el archivo manager.py
  
  # PRIMER METODO CON def create() => Me quedo con este , mas ordenado y asi puedo crear el update , delete, etc
  # Ese validated_data te imprime o es todos los datos , osea un objeto de los campos con los datos que pongas al crear el usuario {password:"1234", "name":"Cristian"} algo asi , estos campos vienen al crear un usuario 
  def create(self, validated_data):
    validated_data["password"] = make_password(validated_data["password"])
    user = MyUserModel.objects.create(**validated_data)
    return user
  
  # ACTUALIZAR LA CONTRASEÑA => La instancia es la data creada antes
  def update(self, instance, validated_data):
    
    # OJO => el segundo parametro ("name", instance.name) asi en todos los campos,  eso seria para que cuando quieras actualizar solo un campo con el PUTCH , los anteriores tomen su valor creado antes 
    instance.name = validated_data.get("name", instance.name)
    instance.email = validated_data.get("email", instance.email)
    instance.phone = validated_data.get("phone", instance.phone)
    instance.status = validated_data.get("status", instance.status)
    instance.role_id = validated_data.get("role_id", instance.role_id)
    
    if "password" in validated_data:
      instance.password = make_password(validated_data.get("password"))
    
    instance.save()
    return instance
  
  
  #SEGUNDO METODO CON def save() => Aca mismo hacemos el create y update
  # def save(self):
    #---Si esque existe la instancia vamos a actualizar los campos del usuario
    #if self.instance :
      # instance = self.instance
      #---Aca llamamos a todos los campos que nos mandan el usuario 
      # instance.name = self.validated_data.get("name", instance.name)
      # instance.email = self.validated_data.get("email",instance.email)
      # instance.phone = self.validated_data.get("phone", instance.phone)
      # instance.status = self.validated_data.get("status", instance.status)
      # instance.role_id = self.validated_data.get("role_id", instance.role_id)
      
      #--- Validamos que password exista , si existe tmb lo llamamos
      # if "password" in self.validated_data:
        # instance.password = self.validated_data.get("password")
      
      # instance.save()
      # return instance
     
    #---Si esque no existe la instancia vamos a crear el usuario
    #else: 
      # user = MyUserModel(**self.validated_data)
      #---Pasamos el password para encriptarlo , ese password que esta ahi es el password que esta en la validacion
      # user.set_password(self.validated_data.get("password"))
      # user.save()
      # return user
      
  
# Este serializer es para hacer nuestra ruta login personalizado
class LoginSerializer(TokenObtainPairSerializer): 
  # Lo que hacemos con esto es validar si el usuario esta activo o no
  # OJO => attrs (que son los datos de inicio de sesión) 
  def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
    # Construimos un diccionario authenticate_kwargs con las credenciales proporcionadas (email y contraseña).
    authenticate_kwargs = {
      self.username_field: attrs[self.username_field],
      "password": attrs["password"]
    } 
    
    #Luego se llama a la función authenticate, que verifica si las credenciales son válidas.
    user = authenticate(**authenticate_kwargs)
    
    # Si el usuario es válido y está activo, genera y devuelve el token access y actualización, lo que permitirá que el usuario se loguee exitosamente
    if user and user.status:
      # Este metodo  genera los tokens JWT necesarios para (loguearse) solo si lo de arriba es true 
      return super().validate(attrs)

    # Si esque no esta activo o no existe no dejara loguearse
    raise ValidationError("La cuenta de usuario está deshabilitada")
  
  @classmethod
  def get_token(cls, user):
    # Se llama al método super().get_token(user), que genera un token JWT básico con la información predeterminada (por ejemplo, el ID del usuario).
    token = super().get_token(user)

    # Luego le añadimos campos adicionales
    token["email"] = user.email
    token["name"] = user.name
    
    #Resultado: Cuando el token se genera, además de la información predeterminada como el ID del usuario, también incluye el correo electrónico y el nombre del usuario. Si abres el token en jwt.io, podrás ver estos valores adicionales en su payload.
    return token
  
