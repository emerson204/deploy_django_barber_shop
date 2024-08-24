from django.urls import path
from .views import *

urlpatterns = [
  # Rutas para Servicios
  path("list/", ServiceListView.as_view()),
  path("create/", ServiceCreateView.as_view()),
  path("update/<int:pk>/", ServiceUpdateView.as_view()),

  # Rutas para Barberos
  path("barber/list/", BarberListView.as_view()),
  path("barber/create/", BarberCreateView.as_view()),
  path("barber/update/<int:pk>/", BarberUpdateView.as_view()),
  path("barber/delete/<int:pk>/", BarberDeleteView.as_view()),
  path("barber/available/<int:day>/<str:hour>", BarberAvailableView.as_view()), # Ruta para la disponibiliadad del barbero
  
  # Ruta para schedules
  path("schedule/list/", ScheduleListView.as_view()),
  path("shcedule/create/", ScheduleCreateView.as_view()),
  path("schedule/update/<int:pk>/", ScheduleUpdateView.as_view()),
  path("schedule/delete/<int:pk>", ScheduleDeleteView.as_view())
]
