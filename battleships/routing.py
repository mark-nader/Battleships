from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from game import consumers

channel_routing = [
	route_class(consumers.LobbyConsumer,  path=r"^/lobby/"),
	route_class(consumers.GameConsumer,  path=r"^/game/(?P<game_id>\d+)/$")
]

application = ProtocolTypeRouter({})
