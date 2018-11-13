from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class start(Page):
    def is_displayed(self):
        return (self.player.round_number==1)
    def before_next_page(self):
        self.participant.vars['bid_stage'] = True
        self.participant.vars['result_stage'] = False

class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']
    def is_displayed(self):
        return self.participant.vars['bid_stage']

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
class FinalPage(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    start,
    Bid,
    PostBidWaitPage,
    LastRoundResults,
    FinalPage,
]
