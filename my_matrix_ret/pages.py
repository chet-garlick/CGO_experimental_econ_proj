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
		self.participant.vars['out_of_time_first_task'] = time.time() + self.player.task_timer
		
	def vars_for_template(self):

		return {
			'debug': settings.DEBUG,  
		}

class instructions_quiz_page(Page):
	def is_displayed(self):
		return self.round_number == 2
			
		
		
		
class first_task_page(Page):
	form_model = models.Player
	form_fields = ['user_input']
	
	timer_text = 'Time left to complete matrices:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_first_task'] - time.time()
		
	def is_displayed(self):
		#print (self.participant.vars['out_of_time_first_task'] - time.time()) This prints time remaining to the command line. I used this to test the timer.
		return (self.participant.vars['out_of_time_first_task'] - time.time() > 0 and self.round_number > 2)
		#The above line returns true if the statements on either side of the 'and' operator return true. 
		#This means that the is_displayed funtion will only return true (and display this page) if self.round_number is greater than two and there is still time left on the timer.
		
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		total_payoff = 0
		for p in self.player.in_all_rounds():
			if p.payoff_score != None: 
				total_payoff += p.payoff_score

			if self.round_number == 3: #on very first task dont display the correctness of previous answer.
					correct_last_round = "<br>"
			else: #all subsequent tasks displace the correctness of previous answer.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'total_payoff': round(total_payoff),
			'problems_attempted_first_task':(self.round_number - 3), 
			#The -3 on the line above comes from the number of pages rounds before the task begins, so the instructions_quiz_page, etc. don't count as missed problems.
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
			if (prev_player.user_input != None):
				if (prev_player.user_input > 0):
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
	start_page,
	first_task_page,
	instructions_quiz_page,
	Results
    #"""MyPage,
    #ResultsWaitPage,
    #Results"""
	#TODO:: Write correct page sequence. Probably just start_page, then task_page, then results page? 
]
