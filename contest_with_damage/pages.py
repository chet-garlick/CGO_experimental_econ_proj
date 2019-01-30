from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class start(Page):
    def is_displayed(self): #Only show the start page on the first round.
        return (self.player.round_number==1)

class Bid(Page):
    form_model = 'player' #oTree specific syntax connecting the player to the page.
    form_fields = ['bid_amount'] #oTree specific syntax connecting the player's input to the players 'bid_amount' data field.

    def vars_for_template(self):
        partner = self.player.get_partner()
        return {
            'player_history':self.player.in_all_rounds(),
        }

class PostBidWaitPage(WaitPage):
    def after_all_players_arrive(self): #When all of the players show up, determine the winner and set their relevant payoffs.
        self.group.set_winner()
        for p in self.group.get_players():
            if p.is_winner: p.set_payoff(self.group.lowest_bid)
            else: p.set_payoff(self.group.highest_bid)


class LastRoundResults(Page):
    def vars_for_template(self):
        partner = self.player.get_partner()
        return {
            'player_history':self.player.in_all_rounds(),
            'partner_history':partner.in_all_rounds(),
        }

    def before_next_page(self):
        if(self.round_number==Constants.num_rounds): #If tthat round was the last round, determine the total payoff for that player.
            self.player.determine_total_payoff()

class FinalPage(Page):

    def is_displayed(self): #Display the last page only on the last page.
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    start,
    Bid,
    PostBidWaitPage,
    LastRoundResults,
    FinalPage,
]
