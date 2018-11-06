from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Chet Garlick'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'auction_with_spillover'
	players_per_group = None
	num_rounds = 3
	min_allowable_bid = 0
	max_allowable_bid = 10
	item_value = 5
	initial_player_cash = 10


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	item_value = models.FloatField(
		doc="""Common value of the item to be auctioned, random for treatment""",
		initial=Constants.item_value
	)
	highest_bid = models.FloatField()
	lowest_bid = models.FloatField()
	def set_winner(self):
		players = self.get_players()
		self.highest_bid = max([p.bid_amount for p in players])
		self.lowest_bid = min([p.bid_amount for p in players])
		players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
		winner = random.choice(
			players_with_highest_bid)  # NOTE: need to ask Dr. Rentscher how to handle situation where both people have same bid.
		winner.is_winner = True


class Player(BasePlayer):
	bid_amount = models.FloatField(
		min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
		doc="""Amount bidded by the player"""
	)
	
	is_winner = models.BooleanField(
		initial=False,
		doc="""Indicates whether the player is the winner"""
	)
	
	player_cash = models.FloatField(
		initial = Constants.initial_player_cash
	)
	
	def set_payoff(self, other_bid):
		print(self.round_number)
		if (self.is_winner and self.round_number!=1):
			self.player_cash = self.in_round(self.round_number-1).player_cash + (self.group.item_value - self.bid_amount - other_bid)
		elif(self.is_winner and self.round_number==1):
			self.player_cash += (self.group.item_value - self.bid_amount - other_bid)
		elif(not self.is_winner and self.round_number!=1):
			self.player_cash = self.in_round(self.round_number-1).player_cash - (self.bid_amount + other_bid)
		else:
			self.player_cash -= (self.bid_amount + other_bid)
		for p in self.in_all_rounds():
			p.player_cash = self.player_cash
			
			
			
			
			
			
			
			
			