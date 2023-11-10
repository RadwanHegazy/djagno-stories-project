from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('status/<str:useruuid>/',views.status,name='status'),
    path('upload/status/',views.upload_status,name='upload_status'),
]