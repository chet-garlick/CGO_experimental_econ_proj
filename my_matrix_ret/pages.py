from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models
from django.conf import settings
import time
import random

class start_page(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
		self.participant.vars['out_of_time'] = time.time() + self.player.task_timer
		
    def vars_for_template(self):

        return {
            'debug': settings.DEBUG,  
        }

class task_page(Page):
	form_model = models.Player
	form_fields = ['user_input']
	
	def get_seconds_left(self):
		return self.participant.vars['out_of_time'] - time.time()
		
	def is_displayed(self):
		print self.participant.vars['out_of_time'] - time.time() > 3
        return self.participant.vars['out_of_time'] - time.time() > 3
		
	def vars_for_template(self):
		total_payoff = 0
		for p in self.player.in_all_rounds():
            if p.payoff_score != None: 
                total_payoff += p.payoff_score

				if self.round_number == 1: #on very first task
            correct_last_round = "<br>"
        else: #all subsequent tasks
            if self.player.in_previous_rounds()[-1].is_correct:
                correct_last_round = "Your last sum was <font color='green'>correct</font>"
            else: 
                correct_last_round = "Your last sum was <font color='red'>incorrect</font>"
        
        return {
            'total_payoff': round(total_payoff),
            'round_count':(self.round_number - 1),
            'debug': settings.DEBUG,
            'correct_last_round': correct_last_round,        
        }

				
	def before_next_page(self):
        self.player.score_round()

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
	def is_displayed(self):
		return self.round_number == Constants.num_rounds
		
	def vars_for_template(self):

        total_payoff = 0
        for p in self.player.in_all_rounds():
            if p.payoff_score != None: 
                total_payoff += p.payoff_score

        self.participant.vars['task_1_score'] = total_payoff

        # only keep obs if YourEntry player_sum, is not None. 
        table_rows = []
        for prev_player in self.player.in_all_rounds():
            if (prev_player.user_total != None):
                if (prev_player.user_total > 0):
                    row = {
                        'round_number': prev_player.round_number,
                        'int1': prev_player.int1,
                        'int2': prev_player.int2,
						'int3': prev_player.int3,
						'int4': prev_player.int4,
						'int5': prev_player.int5,
						'int6': prev_player.int6,
						'int7': prev_player.int7,
						'int8': prev_player.int8,
						'int9': prev_player.int9,
						'int10': prev_player.int10,
						'int11': prev_player.int11,
						'int12': prev_player.int12,
						'int13': prev_player.int13,
						'int14': prev_player.int14,
						'int15': prev_player.int15,
						'int16': prev_player.int16,
						'int17': prev_player.int17,
						'int18': prev_player.int18,
						'int19': prev_player.int19,
						'int20': prev_player.int20,
						'int21': prev_player.int21,
						'int22': prev_player.int22,
						'int23': prev_player.int23,
						'int24': prev_player.int24,
						'int25': prev_player.int25,
						
						
                        'number_of_ones': prev_player.solution,
                        'player_input': round(prev_player.user_input),
                        'is_correct':prev_player.is_correct,
                        'payoff': round(prev_player.payoff_score),
                    }
                    table_rows.append(row)

        self.participant.vars['t1_results'] = table_rows

        return {
        'table_rows': table_rows,
        'total_payoff':round(total_payoff),
        }
		


page_sequence = [
    """MyPage,
    ResultsWaitPage,
    Results"""
	#TODO:: Write correct page sequence. Probably just start_page, then task_page, then results page? 
]
