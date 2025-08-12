from django.urls import path
from . import views

urlpatterns = [
    path("scan/", views.scan_page, name="scan_page"),
    path("upload_qr/", views.upload_qr, name="upload_qr"),
]
