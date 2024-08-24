from django.contrib.auth.models import BaseUserManager

# Esto es para personalizar nuestro user que viene por defecto en django , en la tabla users de la base de datos

# Lo que hace esto es recibir los datos de un usuario cuando nosotros vallamos a crear este usuario y una vez que reciba los datos , email , password y los otros datos , primero comprobamos el email con el if not 
# Luego pasamos tanto el email tanto como los otros datos en self.model , esa instancia estaria guardado en la variable user
# Luego pasamos la contraseña con el set_password , ese metodo es propio de django y tmb se encarga de encriptar la contra 
#  Finalmente guardamos el usuario en la base de datos con el save()

class UserManager(BaseUserManager):
  def create_user(self, email , password , **extra_fields):
    
    # Aca validamos que el email sea requerido
    if not email:
      raise ValueError("Email required")

    # Aca pasamos el email y los otros datos con **extra_fields y eso se guardaria en la variable user
    user = self.model(
      email = self.normalize_email(email)
      **extra_fields
    )
    
    # Como vez arriba no le pasamos la password , porque django tiene el metodo set_password para hacerlo directamente desde aca
    user.set_password(password)
    
    # Con esto mandamos los datos a la base de datos con el save()
    user.save(using=self._db)
    
    return user
  
  
  def create_superuser(self, email , password=None):
    # Este create_user no es el metodo de arriba , es un metodo propio de django
    user = self.create_user(
      email = email,
      password = password
    )
    
    # Este is_superuser es la columna que creamos en MyUserModel en models.py de Authentication
    user.is_superuser = True 
    user.save(using=self._db)
    
    return user