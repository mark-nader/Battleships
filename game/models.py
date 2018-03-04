from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from channels import Group
import json
from datetime import datetime

class Game(models.Model): 
	p1 = models.ForeignKey(User, related_name='p1') 
	p2 = models.ForeignKey(User, related_name='p2', null=True, blank=True) 
	num_cols = models.IntegerField(default=10) 
	num_rows = models.IntegerField(default=10) 
	player_turn = models.IntegerField(default=1) 
	p1_ship_count = models.IntegerField(default=10)
	p2_ship_count = models.IntegerField(default=10)
	p1_ready = models.BooleanField(default=false)
	p2_ready = models.BooleanField(default=false)
	
	def get_available_games():
		return Game.objects.filter(p2=None)
	
	def get_game(game_id):
		return Game.objects.get(pk=game_id)

	def create_new_game(user, cols, rows, ships):
		new_game = Game(p1=user, player_turn=1, num_cols=cols, num_rows=rows,
						player_turn=1, p1_ship_count=ships, p2_ship_count=ships, p1_ready=false, p2_ready=false)
		new_game.save()
		return new_game
	
	def add_p2(game_id,p2_id):
		Game.objects.get(pk=game_id).update(p2=p2_id)
	
	def set_next_turn(game_id):
		Game.objects.get(pk=game_id).update(player_num=3-F('player_turn'))
	
	def set_ship_count(game_id, player_id, new_count):
		game = Game.objects.get(pk=game_id)
		if player_id == game.p1:
			game.update(p1_ship_count=new_count)
		if player_id == game.p2:
			game.update(p2_ship_count=new_count)
	
	def get_both_ready(game_id):
		game = Game.objects.get(pk=game_id)
		return game.p1_ready && game.p2_ready
	
	def set_ready(game_id, player_id):
		game = Game.objects.get(pk=game_id)
		if player_id == game.p1:
			game.update(p1_ready=true)
		if player_id == game.p2:
			game.update(p2_ready=true)
	
	
class Cell(models.Model): 
	game = models.ForeignKey(Game) 
	user_owner = models.ForeignKey(User)
	board_type = models.IntegerField(default=0)
	x = models.IntegerField(default=0)
	y = models.IntegerField(default=0) 
	state = models.CharField(max_length=20, default='sea') 
	ship_or_sea = models.ForeignKey(User_Shipyard)
	
	def get_cell(game_id, user, row, col): 
		return Cell.objects.get(game=game_id, user_owner=user, x=col, y=row)
	
	def set_cell_state(game_id, user, row, col, player_num, new_state): 
		Cell.objects.get(game=game_id, user_owner=user, x=col, y=row).update(state=new_state)
	
	def create_new_board(game_id, rows, cols, p1_id, p2_id):
		for player_id in [p1_id, p2_id]:
			for type in [1, 2]:
				if type == 1: cell_state = 'sea'
				else: cell_state = 'unknown'
				for r in range(0, rows):
					for c in range(0, cols):
						new_square = Cell(game=game_id, user_owner=player_id, board_type=type, x=c, y=r, state=cell_state, ship_or_NULL=NULL)
						new_square.save() 
	
	def place_part_of_ship(game_id, user_owner, row, col, user_ship_id):
		Cell.objects.get(game=game_id, user_owner=user, board_type=1 x=col, y=row).update(ship_or_NULL=user_ship_id)
		
	

class Shipyard(models.Model):
	length = models.IntegerField(default=3)
	name = models.CharField(max_length=20)
	
	def get_ship(ship_id):
		return Shipyard.objects.get(pk=ship_id)
	
	def add_new_ship(ship_length,ship_name):
		Shipyard(length=ship_length, name=ship_name).save()
		
	def delete_ship_by_id(ship_id):
		Shipyard.objects.get(pk=ship_id).delete()
		
	def delete_ships_by_length(ship_length):
		Shipyard.objects.filter(length=ship_length).delete()
	
	def get_all_ships():
		return Shipyard.objects

class User_Shipyard(models.Model):
	user = models.ForeignKey(User)
	ship = models.ForeignKey(Shipyard)
	hit_count = models.IntegerField(default=0)
	
	def add_user_ship(user_id,ship_id):
		User_Shipyard(user_id,ship_id,0).save()
		
	def delete_user_ship(user_id,ship_id):
		User_Shipyard.objects.get(user=user_id,ship=ship_id).delete()
		
	def get_user_shipyard_size(user_id)
		return User_Shipyard.objects.filter(user=user_id).count()
