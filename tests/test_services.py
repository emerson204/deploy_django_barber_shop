
import pytest 
from rest_framework.test import APIClient
from rest_framework import status 


@pytest.fixture
def client_with_token():
  client = APIClient()
  
  role_data = {
    "name": "ADMIN"
  
  }
  role = client.post("/api/v1/authentication/role/create/", role_data , format="json")
  
  if role.status_code != status.HTTP_201_CREATED:
    raise Exception("No se pudo crear el rol")
  
  user_data = {
    "name": "Drago",
    "email": "drago@gmail.com",
    "password": "drago",
    "phone": "123456789",
    "role_id": 1
  }
  
  user = client.post("/api/v1/authentication/user/create/", user_data , format="json")
  
  if user.status_code != status.HTTP_201_CREATED:
    raise Exception("No se pudo crear el usuario")
  
  credenciales = {
    "email": user_data["email"],  
    "password": user_data["password"]
  }
  
  response = client.post("/api/v1/authentication/login/", credenciales , format="json")
  
  if response.status_code != status.HTTP_200_OK:
    raise Exception("No se pudo iniciar la sesión")
  
  client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
  
  return client

@pytest.mark.django_db
def test_services_list(client_with_token):
  response = client_with_token.get("/api/v1/services/list/")
  
  assert response.status_code == status.HTTP_200_OK
  assert response.data["message"] == "Servicios obtenidos correctamente"
  
  