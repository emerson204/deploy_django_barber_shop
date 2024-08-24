from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import *
from .serializer import *

from datetime import time

# RUTAS PARA SERVICES

class ServiceListView(generics.ListAPIView):
  queryset = ServiceModel.objects.all()
  serializer_class = ServiceSerializer 
  # permission_classes = [IsAuthenticated]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Servicios obtenidos correctamente",
      "data": response.data
    }, status=status.HTTP_200_OK)
    

class ServiceCreateView(generics.CreateAPIView):
  serializer_class = ServiceSerializer
  permission_classes = [IsAuthenticated]
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Servicio creado correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
    
class ServiceUpdateView(generics.UpdateAPIView):
  queryset = ServiceModel.objects.all()
  serializer_class = ServiceSerializer
  permission_classes = [IsAuthenticated]
  
  def update(self, request, *args, **kwargs):
    try:
      response = super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Servicio actualizado correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Servicio no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)


# RUTAS PARA BARBERS
class BarberListView(generics.ListAPIView):
  queryset = BarberModel.objects.all()
  serializer_class = BarberSerializer
  permission_classes = [IsAuthenticated]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Barberos obtenidos correctamente",
      "data": response.data  
    }, status=status.HTTP_200_OK)

class BarberCreateView(generics.CreateAPIView):
  serializer_class = BarberSerializer
  permission_classes = [IsAuthenticated]
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    
    return Response({
      "message": "Barbero creado correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)
    
class BarberUpdateView(generics.UpdateAPIView):
  queryset = BarberModel.objects.all()
  serializer_class = BarberSerializer 
  permission_classes = [IsAuthenticated]
  
  def update(self, request, *args, **kwargs):
    try:
      response =  super().update(request, *args, **kwargs)
      
      return Response({
        "message": "Barbero actualizado correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Barbero no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
    
class BarberDeleteView(generics.DestroyAPIView):
  queryset = BarberModel.objects.all()
  serializer_class = BarberSerializer
  
  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.status = False 
      instance.save()
      
      serializer = self.get_serializer(instance)
      
      return Response({
        "message": "Barbero eliminado correctamente",
        "data": serializer.data
      }, status=status.HTTP_200_OK)
      
    except Http404:
      return Response({
        "message": "Barbero no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
  

# El propósito de esta vista es devolver una lista de barberos que estén disponibles en una fecha y hora específicas.
class BarberAvailableView(generics.ListAPIView):
  serializer_class = BarberSerializer
  
  def get_queryset(self):
    #Obtiene el valor de day (día) desde los argumentos de la URL
    day = self.kwargs["day"]
    #Obtiene el valor de hour (hora) desde los argumentos de la URL.
    hour = self.kwargs["hour"]
    #Convierte el parámetro hour de formato de cadena a un objeto de tipo time (por ejemplo, convierte "14:30" en un objeto time que representa las 2:30 PM).
    hour_time = time.fromisoformat(hour)
    
    #Se hace una consulta a la base de datos buscando los barberos que tienen un horario que coincide con el día y la hora proporcionado basandose en la informacion de sus horarios(schedules)
    available_barbers = BarberModel.objects.filter(
      # Filtra los barberos cuyo día de trabajo coincide con el día proporcionado (day).
      #Ejemplo: Si day es "lunes" (día 1 en la semana), este filtro seleccionará solo a los barberos que tienen algún horario registrado para el lunes.
      schedules__day_of_week = day,
      #Filtra los barberos cuyo horario de trabajo comienza antes o exactamente a la hora proporcionada (hour_time).
      #Si hour_time es "14:00" (2:00 PM), este filtro selecciona a los barberos cuyo turno empieza antes o a las 2:00 PM.
      schedules__start_time__lte = hour_time,
      # Filtra los barberos cuyo horario de trabajo termina después o exactamente a la hora proporcionada (hour_time).
      #Ejemplo: Si hour_time es "14:00" (2:00 PM), este filtro selecciona a los barberos cuyo turno termina a las 2:00 PM o más tarde
      schedules__end_time__gte = hour_time
    ).distinct() # Elimina los duplicados. Si un barbero aparece más de una vez en los resultados, distinct() asegura que solo se retorne una vez, aunque tenga múltiples turnos que coincidan con los criterios.
  
    return available_barbers

  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    
    return Response({
      "message": "Barbero encontrado con exito",
      "data": response.data
    }, status=status.HTTP_200_OK)


# RUTAS PARA SCHEDULES 

class ScheduleListView(generics.ListAPIView):
  queryset = ScheduleModel.objects.all()
  serializer_class = ScheduleSerializer
  permission_classes = [IsAuthenticated]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)

    return Response({
      "message": "Schedules obtenidos correctamente",
      "data": response.data
    }, status=status.HTTP_200_OK)
    
class ScheduleCreateView(generics.CreateAPIView):
  serializer_class = ScheduleSerializer
  permission_classes = [IsAuthenticated]
  
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)

    return Response({
      "message": "Schedule creado correctamente",
      "data": response.data
    }, status=status.HTTP_201_CREATED)


class ScheduleUpdateView(generics.UpdateAPIView):
  queryset = ScheduleModel.objects.all()
  serializer_class = ScheduleSerializer
  permission_classes = [IsAuthenticated]
  
  
  def update(self, request, *args, **kwargs):
    try: 
      response = super().update(request, *args, **kwargs)

      return Response({
        "message": "Schedule actualizado correctamente",
        "data": response.data
      }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "message": "Schedule no encontrado"
      }, status=status.HTTP_404_NOT_FOUND)
    
class ScheduleDeleteView(generics.DestroyAPIView):
  queryset = ScheduleModel.objects.all()    

  def destroy(self, request, *args, **kwargs):
    try:
      response = super().destroy(request, *args, **kwargs)
      
      return Response({
        "message": "Schedule eliminado correctamente",
        "data": response.data 
      }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "message" : "Schedule no encontrado"
      },status=status.HTTP_404_NOT_FOUND)