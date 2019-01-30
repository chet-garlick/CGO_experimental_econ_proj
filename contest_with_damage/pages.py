from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class start(Page):
    def is_displayed(self):
        return (self.player.round_number==1)

class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']

    def vars_for_template(self):
        partner = self.player.get_partner()
        return {
            'player_history':self.player.in_all_rounds(),
        }

class PostBidWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winner()
        for p in self.group.get_players():
            if p.is_winner: p.set_payoff(self.group.lowest_bid)
            else: p.set_payoff(self.group.highest_bid)


class LastRoundResults(Page):
    def vars_for_template(self):
        partner = self.player.get_partner()
        return {
            'player_history':self.player.in_all_rounds(),
        }

    def before_next_page(self):
        if(self.round_number==Constants.num_rounds):
            self.player.determine_total_payoff()

class FinalPage(Page):

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.determine_total_payoff()


page_sequence = [
    start,
    Bid,
    PostBidWaitPage,
    LastRoundResults,
    FinalPage,
]
