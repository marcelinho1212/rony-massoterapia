from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("agendar/", views.choose_professional, name="choose_professional"),
    path("agendar/<slug:professional_slug>/servicos/", views.choose_service, name="choose_service"),
    path("agendar/<slug:professional_slug>/servicos/<int:service_id>/horarios/", views.choose_slot, name="choose_slot"),
    path("agendar/confirmar/", views.confirm_booking, name="confirm_booking"),
    path("sobre/", views.about, name="about"),
]
