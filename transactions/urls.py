from django.urls import path
from .views import *

urlpatterns = [
    # Rutas para las citas
    path("appointment/create/", AppointmentCreateView.as_view()),
    path("appointments/list/", AppointmentListView.as_view()),

    # Rutas para las transacciones
    path("payment/list/", PaymentListView.as_view()),
    path("payment/create/", PaymentCreateView.as_view()),
    path("payment/verify/", PaymentNotificationView.as_view()),
    path("payment/update/<int:pk>/", PaymentUpdateView.as_view()),
    path("payment/delete/<int:pk>/", PaymentDeleteView.as_view()),
    
    
    path("invoice/create/<int:appointment_id>", InvoiceCreateView.as_view()),
    path("invoice/find/<int:tipo_de_comprobante>/<str:serie>/<int:numero>/", InvoiceRetrieveView.as_view())
]
