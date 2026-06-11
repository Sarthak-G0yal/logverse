from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/mock-log/', views.ingest_log, name='ingest_log'),
]