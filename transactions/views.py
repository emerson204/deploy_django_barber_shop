from .models import *
from .serializer import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from authentication.permission import IsAdmin, IsAutenticado, IsClient

import os
import requests
from datetime import datetime
from django.shortcuts import get_object_or_404

import mercadopago

# RESERVAR LA CITA
# Comprobar disponibilidad de los barberos y sus horarios para x dia y x hora
class AppointmentCreateView(generics.CreateAPIView):
  serializer_class = AppointmentSerializer
  permission_classes = [IsAutenticado, IsClient]
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Cita reservada correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
  
class AppointmentListView(generics.ListAPIView):
  queryset = AppointmentModel.objects.all()
  serializer_class = AppointmentSerializer
  permission_classes = [IsAutenticado, IsAdmin]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Citas obtenidas correctamente",
      "data": response.data
    }, status=status.HTTP_200_OK)
  
  
# RUTAS PARA EL PAYMENT (PAGO)

class PaymentListView(generics.ListAPIView):
  queryset = PaymentModel.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsAutenticado, IsAdmin]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Pagos obtenidos correctamente",
      "data": response.data
    }, status=status.HTTP_200_OK)
    
class PaymentCreateView(generics.CreateAPIView):
  serializer_class = PaymentSerializer
  # permission_classes = [IsAutenticado]
  
  def create(self, request, *args, **kwargs):
    
    # Aqui empieza MERCADO PAGO
    token = os.environ.get("MERCADOPAGO_TOKEN")
    mp = mercadopago.SDK(token) 
    
    # Esto es para que aparezcan los detalles de pago en mercado pago 
    preference = {
      "items": [
        {
          "id":1,
          "title": "Corte de cabello",
          "quantity":1,
          "currency_id": "MXN",
          "unit_price": 25,
        }
      ],
      "notification_url": "http://localhost:8000/api/v1/transactions/payment/verify/"
    }
    
    mp_response = mp.preference().create(preference)
    
    print(mp_response)
    
    # response =super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Pago realizado correctamente",
      # "data": response.data
      "data": mp_response
    }, status=status.HTTP_201_CREATED)
    

class PaymentNotificationView(APIView):
  def post(self, request):
    print(request.data)
    print(request.query_params)
    
    return Response({
      "message": "Notificación recibida"
    })

class PaymentUpdateView(generics.UpdateAPIView):
  queryset = PaymentModel.objects.all()
  serializer_class = PaymentSerializer
  permission_classes = [IsAutenticado]
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Cita actualizada correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Cita no encontrada"
      }, status=status.HTTP_404_NOT_FOUND)
      
  
class PaymentDeleteView(generics.DestroyAPIView):
  queryset = PaymentModel.objects.all()
  permission_classes = [IsAutenticado]
    
  def delete(self, request, *args, **kwargs):
    try: 
      super().delete(request, *args, **kwargs)
    
      return Response({
        "message": "Cita eliminada correctamente",
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Cita no encontrada"
      }, status=status.HTTP_404_NOT_FOUND)
      
    
class InvoiceCreateView(APIView):
  def post(self, request, appointment_id):
    try:
      # Con esto y el appointment_id de parametro definida en la ruta en urls.py , ese appointment en models.py tiene service_id , ese servicio tiene los datos como precio , descripcion y todo con respecto al corte.
      # Al hace esto nosotros vamos a pasarle dinamicamente los datos de nuestro servicio para que la boleta salga con los precios del servicio 
      # Y para crear la boleta tenemos que pasarle en el swagger el id del appointment , osea si el servicio es id 2 , pero el appoinment es id 1 , chaparemos ese servicio del id 2 ingresando el id del appointement que es el 1
      appointment = get_object_or_404(AppointmentModel, id=appointment_id)
      
      # subtotal = total / 1.18
      total = appointment.service_id.price
      subtotal = total / 1.18
      igv = total - subtotal
      
      item =  {
            "unidad_de_medida": "ZZ",
            "codigo": "C001",
            "descripcion": appointment.service_id.description,
            "cantidad": 1,
            "valor_unitario": subtotal,
            "precio_unitario": total,
            "subtotal": subtotal,
            "tipo_de_igv": 1,
            "igv": igv,
            "total": total,
            "anticipo_regularizacion": False
      }
      
      # Aqui vamos a generar nuestras facturas electronicas
      url = os.environ.get("NUBEFACT_URL")
      token = os.environ.get("NUBEFACT_TOKEN")
      print(url)
      print(token)
      
      invoice_data = {
        "operacion": "generar_comprobante",
        "tipo_de_comprobante": 2,
        "serie": "BBB1",
        "numero": 1,
        "sunat_transaction": 1,
        "cliente_tipo_de_documento": 1,
        "cliente_numero_de_documento": "00000000",
        "cliente_denominacion": "CLIENTE DE PRUEBA",
        "cliente_direccion": "Av. Larco #44",
        "cliente_email": "email@email.com",
        "fecha_de_emision": datetime.now().strftime("%d-%m-%Y"),
        "moneda": 1,
        "porcentaje_de_igv": 18.0,
        "total_gravada": subtotal,
        "total_igv": igv,
        "total": total,
        "enviar_automaticamente_a_la_sunat": True,
        "enviar_automaticamente_al_cliente": True,
        "items": [item]
      }
      
      nubefact_response = requests.post(url=url, headers={
        "Authorization": f"Bearer {token}"
      }, json=invoice_data)
      
      nubefact_response_json = nubefact_response.json()
      nubefact_response_status = nubefact_response.status_code
      print(nubefact_response_json)
      
      if nubefact_response_status != 200 :
         raise Exception(nubefact_response_json["errors"])
      
      return Response({
        "message": "Documento generado correctamente",
        "data": nubefact_response_json
      }, status=status.HTTP_200_OK)
      
    except Exception as e:
      return Response({
        "message": str(e.args[0])
      },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Esta ruta es para buscar una factura o boleta que hemos generado anteriormente
class InvoiceRetrieveView(APIView):
  def get(self, request, tipo_de_comprobante: int, serie: str, numero: int):
    try:
      url = os.environ.get("NUBEFACT_URL")
      token = os.environ.get("NUBEFACT_TOKEN")
      
      body = {
        "operacion" : "consultar_comprobante",
        "tipo_de_comprobante" : tipo_de_comprobante,
        "serie": serie,
        "numero": numero
      }
      
      nubefact_response = requests.post(
        url = url,
        headers={
        "Authorization": f"Bearer {token}"
        },
        json = body  
      )
      
      nubefact_response_status = nubefact_response.status_code
      nubefact_response_json = nubefact_response.json()
      
      if nubefact_response_status != 200 :
        raise Exception(nubefact_response_json["errors"])
      
      
      return Response({
        "message": "Documento generado correctamente",
        "data": nubefact_response_json
      }, status=status.HTTP_200_OK)
      
    except Exception as e:
      return Response({
        "message": str(e.args[0])
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)