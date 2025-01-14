import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from base.routing import websocket_urlpatterns

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

# Create the Django ASGI application
django_asgi_app = get_asgi_application()

# Define the protocol type router
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # HTTP protocol
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Define WebSocket routes
        )
    ),
})
