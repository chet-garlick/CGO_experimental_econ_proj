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
    beta = 1 #IMPORTANT PARAMETERS
    alpha = 1 #IMPORTANT PARAMETERS
    item_value = 5 #value of the item that participants are competing for. In this case, this will be held constant throughout the experiment.
    initial_player_cash = 10 #some initial starting value for the amount of money participants start with.
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
        initial = Constants.initial_player_cash
    )
    
    round_payoff = models.CurrencyField(
        initial = 0
    )
    def set_payoff(self, other_bid): #This function determines the amount of remaining cash a player has at the end of each round. It is also passed the parameter other_bid, which is the value of the other player's bid that round. 
        #We need to handle things differently if A, the player won that round and B, it is the first round or not.
        if (self.is_winner and self.round_number!=1):  #For rounds past round 1, the winner's remaining cash is their amount of cash last round plus the value of the good minus their bid minus their oppoenents bid.
            self.round_payoff = self.group.item_value - (Constants.alpha * self.bid_amount) - (Constants.beta * self.others_bid_amount)        
            self.player_cash = self.in_round(self.round_number-1).player_cash + self.round_payoff
        elif(self.is_winner and self.round_number==1): #For the first round, there is no previous round to access, so the winner's cash is the cash they have that round.
            self.round_payoff = self.group.item_value - (Constants.alpha * self.bid_amount) - (Constants.beta * self.others_bid_amount)
            self.player_cash = self.player_cash + self.round_payoff
        elif(not self.is_winner and self.round_number!=1): #For the player that is not the winner, is is exactly the same but they do not gain the item value. 
            self.round_payoff = 0 - (Constants.alpha * self.bid_amount) - (Constants.beta * self.others_bid_amount)
            self.player_cash = self.in_round(self.round_number-1).player_cash + self.round_payoff
        else:
            self.round_payoff = 0 - (Constants.alpha * self.bid_amount) - (Constants.beta * self.others_bid_amount)
            self.player_cash = self.player_cash + self.round_payoff

    def get_partner(self): #This function grabs the other player from the pair of players so we can build the history table.
        return self.get_others_in_group()[0]       
          