

from channels.generic.websocket import JsonWebsocketConsumer

#========================================
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#MOST OF THIS IS THE SAME AS THE TUTORIAL
#PROBABLY CANT RUN I WILL TRY AND GET IT
#WORKING WHEN I KNOW MORE ABOUT WHAT IS
#NEEDED TO BE ADDED OR CHANGED
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#========================================

class LobbyConsumer(JsonWebsocketConsumer):

	# Set to True to automatically port users from HTTP cookies
	# (you don't need channel_session_user, this implies it)
	http_user = True


	def connection_groups(self, **kwargs):
		"""
		Called to return the list of groups to automatically add/remove
		this connection to/from.
		"""
		return ["lobby"]

	def connect(self, message, **kwargs):
		"""
		Perform things on connection start
		"""
		pass

	def receive(self, content, **kwargs):
		"""
		Called when a message is received with either text or bytes
		filled out.
		"""
		channel_session_user = True

		action = content['action']
		if action == 'create_game':
			Game.create_new_game(self.message.user, content['cols'], content['rows'])
		
		if action == 'join_game':
			Game.add_p2(context['game_id'],self.message.user)
		
	def disconnect(self, message, **kwargs):
		"""
		Perform things on connection close
		"""
		pass

class GameConsumer(JsonWebsocketConsumer):
	# Set to True to automatically port users from HTTP cookies
	# (you don't need channel_session_user, this implies it)
	http_user = True

	def connection_groups(self, **kwargs):
		"""
		Called to return the list of groups to automatically add/remove
		this connection to/from.
		"""
		return ["game-{0}".format(kwargs['game_id'])]

	def connect(self, message, **kwargs):
		"""
		Perform things on connection start
		"""
		pass

	def receive(self, content, **kwargs):
		"""
		Called when a message is received with either text or bytes
		filled out.
		"""
		channel_session_user = True
		action = content['action']
		
		#will fill this in after lobby works

	def disconnect(self, message, **kwargs):
		"""
		Perform things on connection close
		"""
		pass