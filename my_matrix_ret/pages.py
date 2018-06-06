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
		self.participant.vars['out_of_time_first_task'] = time.time() + self.player.first_task_timer
		self.participant.vars['has_message_page_been_shown'] = False
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = False
		self.participant.vars['show_results_page_next'] = False
		self.participant.vars['show_feed_back_page'] = False
		self.participant.vars['out_of_time_second_task'] = 0
		
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
	
	timer_text = 'Time left to solve problems:'
	
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

		
		
class message_page(Page):
	def before_next_page(self):
		self.participant.vars['has_message_page_been_shown'] = True
		self.participant.vars['show_investment_page_next'] = True


	def is_displayed(self):
		if (self.participant.vars['out_of_time_first_task'] - time.time() <= 0):
			return (not self.participant.vars['has_message_page_been_shown'])
		# Not sure about this logic, need to come up with the best way to ensure this page is displayed directly after first_task_page when that timer expires.
		# Maybe the sequencing in 'page_sequence' at the bottom of this file is sufficient.
		# I think adding a boolean to self somewhere or in the larger scope of each player's vars. that marks whether or not this page has been visited will allow us to do that.
		
		
		
class investment_page(Page):

	def is_displayed(self):
		return self.participant.vars['show_investment_page_next'] == True

	def before_next_page(self):
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = True
		self.participant.vars['out_of_time_second_task'] = time.time() + self.player.second_task_timer
		
		
class second_task_page(Page):

	form_model = models.Player
	form_fields = ['user_input']
	
	timer_text = 'Time left to solve problems:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_second_task'] - time.time()
	
	def is_displayed(self):
		return (self.participant.vars['show_second_task_next'] and self.player.second_task_timer>0)
	
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		total_payoff_second_task = 0
		for p in self.player.in_all_rounds():
			if p.second_payoff_score != None: 
				total_payoff_second_task += p.second_payoff_score

			if self.player.problems_attempted_second_task == 1: 
					correct_last_round = "<br>"
			else: #all subsequent tasks displace the correctness of previous answer.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'total_payoff': round(total_payoff_second_task),
			'problems_attempted_second_task':(self.player.problems_attempted_second_task), 
			#The -3 on the line above comes from the number of pages rounds before the task begins, so the instructions_quiz_page, etc. don't count as missed problems.
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,        
		}

				
	def before_next_page(self):
		self.player.score_round_second_task() #Need to write a score_round function for second task.
		if(self.participant.vars['out_of_time_second_task'] - time.time() < 0):
			self.participant.vars['show_feed_back_page'] = True
		
	
	
class feedback_page(Page):


	def is_displayed(self):
		return self.participant.vars['show_feed_back_page']
		
	def before_next_page(self):
		self.participant.vars['show_results_page_next'] = True
		self.participant.vars['show_feed_back_page'] = False

		
		
class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		pass


class Results(Page):
	def is_displayed(self):
		return self.participant.vars['show_results_page_next']
		
	def vars_for_template(self):

		total_payoff = 0
		total_probs_attempted_task_one = 0
		for p in self.player.in_all_rounds():
			if p.payoff_score != None: 
				total_payoff += p.payoff_score
			if p.problems_attempted != None:
				total_probs_attempted_task_one += p.problems_attempted
				

		self.participant.vars['task_1_score'] = total_payoff
		table_rows = []
		for prev_player in self.player.in_all_rounds():
			if (prev_player.user_input != None):
				if (prev_player.user_input > 0):
					row = {
					"""
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
						'payoff': round(prev_player.payoff_score),"""
                        'is_correct':prev_player.is_correct,
                        
                    }
					table_rows.append(row)

		self.participant.vars['t1_results'] = table_rows

		return {
		'table_rows': table_rows,
		'total_payoff':round(total_payoff),
		'problems_attempted_first_task': total_probs_attempted_task_one
		}
		


page_sequence = [
	start_page,
	first_task_page,
	instructions_quiz_page,
	message_page,
	investment_page,
	second_task_page,
	feedback_page,
	Results
]
