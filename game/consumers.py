

from channels.generic.websocket import JsonWebsocketConsumer

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
			clear_user_placed(self.message.user)
		
		if action == 'join_game':
			Game.add_p2(context['game_id'],self.message.user)
			clear_user_placed(self.message.user)
		
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
		
		if action == 'placeship':
			game_id = content['game_id']
			start_row = content['start_row']
			start_col = content['start_col']
			ship_id = content['ship_id']
			game = Game.get_game(game_id)
			ship = Shipyard.get_ship(ship_id)
			if not Game.get_both_ready(game_id):
				ship_count = User_Shipyard.get_user_shipyard_size(self.message.user)
				if ship_count < game.max_ships:
					if not User_Shipyard.contains_user_ship(self.message.user,ship_id):
						User_Shipyard.add_user_ship(self.message.user,ship_id)
						for i in range(0,ship.length):
							x = i
							y = 0
							if content['vertical'] == true:
								x = 0
								y = i
							Cell.set_cell_state(game_id, self.message.user, 1, start_row+y, start_col+x, '{}'.format(ship_id))
						Game.set_ship_count(game_id,self.message.user,ship_count+1)
		
		if action == 'ready_to_start':
			set_ready(content['game_id'], self.message.user)
		
		if action == 'fire':
			game_id = content['game_id']
			row = content['row']
			col = content['column']
			game = Game.get_game(game_id)
			opponent_id = game.p1
			opponent_ship_count = game.p1_ship_count
			player_num = Game.get_player_num(game_id,self.message.user)
			if player_num == 1:
				opponent_id = game.p2
				opponent_ship_count = game.p2_ship_count
			if player_num != 0:
				if game.player_turn == player_num:
					player_cell = Cell.get_cell(game_id, self.message.user, 2, row, col)
					opponent_cell = Cell.get_cell(game_id, opponent_id, 1, row, col)
					if player_cell.state == 'unknown':
						opponent_cell_state = opponent_cell.state
						if opponent_cell_state == 'sea':
							Cell.set_cell_state(game_id, self.message.user, 2, row, col, 'miss')
						else:
							Cell.set_cell_state(game_id, self.message.user, 2, row, col, 'hit')
							ship_id = int(opponent_cell_state)
							User_Shipyard.inc_hit_count(opponent_id,ship_id)
							ship_length = Shipyard.get_ship(ship_id).length
							if ship_length == User_Shipyard.get_ship(opponent_id,ship_id).hit_count:
								Game.set_ship_count(game_id, opponent_id, opponent_ship_count-1)
								#==========================================================
								#i haven't imported Groups but this code still runs somehow
								if opponent_ship_count == 1:
									message = {'winner': '{}'.format(self.message.user)}
									Group('game-{0}'.format(game_id)).send({'text': json.dumps(message)})
								#==========================================================
						Cell.set_cell_state(game_id, opponent_id, 1, row, col, opponent_cell_state+'-fired_at')

	def disconnect(self, message, **kwargs):
		"""
		Perform things on connection close
		"""
		pass
