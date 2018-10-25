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
	num_rounds = 1
	min_allowable_bid = c(0)
	max_allowable_bid = c(10)
	item_value = 10


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	item_value = models.CurrencyField(
		doc="""Common value of the item to be auctioned, random for treatment""",
		initial=Constants.item_value
	)
	highest_bid = models.CurrencyField()
	def set_winner(self):
		players = self.get_players()
		self.highest_bid = max([p.bid_amount for p in players])
		players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
		winner = random.choice(
			players_with_highest_bid)  # NOTE: need to ask Dr. Rentscher how to handle situation where both people have same bid.
		winner.is_winner = True


class Player(BasePlayer):
	bid_amount = models.CurrencyField(
		min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
		doc="""Amount bidded by the player"""
	)
	
	is_winner = models.BooleanField(
		initial=False,
		doc="""Indicates whether the player is the winner"""
	)
	
	def set_payoff(self):
		if self.is_winner:
			self.payoff = self.group.item_value - self.bid_amount
			if self.payoff < 0:
				self.payoff = 0
		else:
			self.payoff = 0