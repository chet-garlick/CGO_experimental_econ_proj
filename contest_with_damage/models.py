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
    num_rounds = 4 #number of rounds participants will engage in
    num_payoff_rounds = 2 #number of rounds that will be paid
    payoff_rounds = random.sample(range(num_rounds),num_payoff_rounds) #payoff_rounds is a list of rounds that is randomly determined at the beginning of each experiment that will be the subset of rounds that the participants are paid for.
    min_allowable_bid = 0
    max_allowable_bid = 10
    delta = 1 #Damage parameter for the winner
    theta = 1 #Damage parameter for the loser
    item_value = 5 #value of the item that participants are competing for. In this case, this will be held constant throughout the experiment.
    initial_cash_per_round = 10 #some initial starting value for the amount of money participants start with.
    players_per_group = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    item_value = models.CurrencyField(
        doc="""Common value of the item to be auctioned, random for treatment""",
        initial=Constants.item_value
    )
    highest_bid = models.CurrencyField() #Variable to store the highest bid from that round.
    lowest_bid = models.CurrencyField() #Variable to store the lowest bid from that round.
    def set_winner(self):
    #This function is called from Pages.py when all players have submitted a bid for that round. It finds the highest and lowest bid for the round and determines the winner.
        players = self.get_players() #Access all players from the Group.
        self.highest_bid = max([p.bid_amount for p in players]) #Find the highest bid among the bids for each player that round.
        self.lowest_bid = min([p.bid_amount for p in players]) #Find the lowest bid among the bids for each player that round.
        players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid] #This matches the players who submitted the highest bid with that bid amount so that we can set the winner.
        winner = random.choice( players_with_highest_bid )  #This randomly selects one player from among the list of players who have the highest bid. This is to account for the situation where both players input the same bid.
        winner.is_winner = True #Accesses the winning player, and sets their is_winner variable to true.
        players.remove(winner)
        loser=players[0]
        winner.others_bid_amount = self.lowest_bid
        loser.others_bid_amount = self.highest_bid

class Player(BasePlayer):
    bid_amount = models.CurrencyField( #variable to hold the submitted bit amount for each player each round.
        min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
        doc="""Amount bid by the player"""
    )

    others_bid_amount = models.CurrencyField(
        doc="""Amount bid by the player's oppoenent."""
    )

    is_winner = models.BooleanField( #variable to hold whether or not the player won that round. Defaults to false, AKA to a loss. It is changed by the set_winner function in the Group model.
        initial=False,
        doc="""Indicates whether the player is the winner"""
    )

    player_cash = models.CurrencyField( #The remaining cash a player has.
        initial = 0
    )

    round_payoff = models.CurrencyField(
        initial = 0
    )
    total_payoff = models.CurrencyField(
        initial = 0,
        doc="""The total amount a player earns during the rounds that were determined to be payoff rounds."""
    )
    def set_payoff(self, other_bid): #This function determines the amount of remaining cash a player has at the end of each round. It is determined by whether or not they won, how much cash is alloted to each player per round, the item value, and the amount each participant bid.
        if (self.is_winner):
            self.round_payoff = Constants.initial_cash_per_round + self.group.item_value -  self.bid_amount - (Constants.delta * self.others_bid_amount)
        elif(not self.is_winner): #For the player that is not the winner, they do not gain the item value and they lose Theta times the others bid amount.
            self.round_payoff = Constants.initial_cash_per_round -  self.bid_amount - (Constants.theta * self.others_bid_amount)

    def get_partner(self): #This function grabs the other player from the pair of players so we can build the history table.
        return self.get_others_in_group()[0]

    def determine_total_payoff(self): #This function loops over all of the rounds that were determined to be payoff rounds and totals the players earnings over those rounds. It runs at the end of the last round.
        for round in Constants.payoff_rounds:
            self.total_payoff += self.in_round(round).round_payoff
