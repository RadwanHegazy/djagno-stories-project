from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/main/", consumers.MainSocket.as_asgi()),
]