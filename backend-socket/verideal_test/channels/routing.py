from django.urls import re_path, path
from channels.routing import ProtocolTypeRouter, URLRouter

from . import consumers

websocket_urlpatterns = [
    path(r'ws/process', consumers.ProcessConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': 
        URLRouter(
            websocket_urlpatterns
        )
    ,
})