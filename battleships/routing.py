from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game import consumers

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^/lobby/", consumers.LobbyConsumer),
            url(r"^/game/(?P<game_id>\d+)/$", consumers.GameConsumer),
        ])
    )
})
