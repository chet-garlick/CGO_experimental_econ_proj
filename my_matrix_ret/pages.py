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
		self.participant.vars['show_first_task_page_next'] = False
		self.participant.vars['out_of_time_first_task'] = 0
		self.participant.vars['show_message_page_next'] = False
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
		
	def before_next_page(self):
		self.participant.vars['out_of_time_first_task'] = time.time() + self.player.first_task_timer
		self.participant.vars['show_first_task_page_next'] = True
			
		
		
		
class first_task_page(Page):
	form_model = models.Player
	form_fields = ['user_input']
	solution=0 #variable containing corect solution for this counting exercise
	m=[] #list containing the list of integers used to populate the counting exercise, named 'm' for 'matrix'
	for i in range(0,25): #for loop that randomly creates 25 ones and zeros then adding them to the list 'm'
		x = random.randint(0,1) #random.randint is comes from python's built in random library, the arguments 0,1 will grab a one or a zero.
		#x = 1 # testing this to see if the correct solution is counted. the line above is what we want to have in production.
		m.append(x) #adds the new random integer to the list 'm'
		solution+=x #increments the solution by the new random integer, either 0 (no change) or 1

	timer_text = 'Time left to solve problems:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_first_task'] - time.time()
		
	def is_displayed(self):
		#print (self.participant.vars['out_of_time_first_task'] - time.time()) This prints time remaining to the command line. I used this to test the timer.
		return (self.participant.vars['out_of_time_first_task'] - time.time() > 0 and self.participant.vars['show_first_task_page_next'])
		#The above line returns true if the statements on either side of the 'and' operator return true. 
		#This means that the is_displayed funtion will only return true (and display this page) if self.round_number is greater than two and there is still time left on the timer.
		
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		total_payoff = 0
		num_attempted = 0
		#solution=0
		#Repeating the logic from the beginning of this class so that every page is different.
		self.solution=0 #variable containing corect solution for this counting exercise
		self.m=[] #list containing the list of integers used to populate the counting exercise, named 'm' for 'matrix'
		for i in range(0,25): #for loop that randomly creates 25 ones and zeros then adding them to the list 'm'
			x = random.randint(0,1) #random.randint is comes from python's built in random library, the arguments 0,1 will grab a one or a zero.
			#x = 1 # testing this to see if the correct solution is counted. the line above is what we want to have in production.
			self.m.append(x) #adds the new random integer to the list 'm'
			self.solution+=x #increments the solution by the new random integer, either 0 (no change) or 1
		for p in self.player.in_all_rounds(): #This loops over every round and totals the payoff scores for each player.
			if p.first_payoff_score != None: 
				total_payoff += p.first_payoff_score 
				num_attempted += p.problems_attempted_first_task
				
			if num_attempted==0: #on very first task dont display the correctness of previous answer.
					correct_last_round = "<br>"
			else: #all subsequent tasks display the correctness of previous answer.
				#using num_attemped as a helper variable so that on the first attempt the user won't see "correctly answered 0 out of None"
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'problems_attempted_first_task':round(num_attempted), 
			'total_payoff': round(total_payoff),
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,
			'int0' : self.m[0],
			'int1' : self.m[1],
			'int2' : self.m[2],
			'int3' : self.m[3],
			'int4' : self.m[4],
			'int5' : self.m[5],
			'int6' : self.m[6],
			'int7' : self.m[7],
			'int8' : self.m[8],
			'int9' : self.m[9],
			'int10' : self.m[10],
			'int11' : self.m[11],
			'int12' : self.m[12],
			'int13' : self.m[13],
			'int14' : self.m[14],
			'int15' : self.m[15],
			'int16' : self.m[16],
			'int17' : self.m[17],
			'int18' : self.m[18],
			'int19' : self.m[19],
			'int20' : self.m[20],
			'int21' : self.m[21],
			'int22' : self.m[22],
			'int23' : self.m[23],
			'int24' : self.m[24],
			'solution' : self.solution
		}

				
	def before_next_page(self):
	
		self.participant.vars['show_message_page_next']=True
		self.player.score_round(self.solution)

		
		
class message_page(Page):
	def before_next_page(self):
		self.participant.vars['show_message_page_next'] = False
		self.participant.vars['show_investment_page_next'] = True


	def is_displayed(self):
		return self.participant.vars['out_of_time_first_task'] - time.time() < 0 and self.participant.vars['show_message_page_next']
		# Not sure about this logic, need to come up with the best way to ensure this page is displayed directly after first_task_page when that timer expires.
		# Maybe the sequencing in 'page_sequence' at the bottom of this file is sufficient.
		# I think adding a boolean to self somewhere or in the larger scope of each player's vars. that marks whether or not this page has been visited will allow us to do that.
		
		
		
class investment_page(Page):

	def is_displayed(self):
		return self.participant.vars['show_investment_page_next']

	def before_next_page(self):
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = True
		self.participant.vars['out_of_time_second_task'] = time.time() + self.player.second_task_timer
		
		
class second_task_page(Page):

	form_model = models.Player
	form_fields = ['user_input']
	solution=0#variable containing corect solution for this counting exercise
	
	timer_text = 'Time left to solve problems:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_second_task'] - time.time()
	
	def is_displayed(self):
		return (self.participant.vars['show_second_task_next'] and self.player.second_task_timer>0)
	
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		self.solution=0
		num_attempted=0
		m=[] #list containing the list of integers used to populate the counting exercise, named 'm' for 'matrix'
		for i in range(0,25): #for loop that randomly creates 25 ones and zeros then adding them to the list 'm'
			x = random.randint(0,1) #random.randint is comes from python's built in random library, the arguments 0,1 will grab a one or a zero.
			m.append(x) #adds the new random integer to the list 'm'
			self.solution+=x #increments the solution by the new random integer, either 0 (no change) or 1
			#print (m[i])
			
		total_payoff_second_task = 0
		for p in self.player.in_all_rounds():
			if p.second_payoff_score != None: 
				total_payoff_second_task += p.second_payoff_score
				num_attempted += p.problems_attempted_second_task

			if num_attempted==0: 
					correct_last_round = "<br>"
			else: #all subsequent tasks displace the correctness of previous answer.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'total_payoff': round(total_payoff_second_task),
			'problems_attempted_second_task':num_attempted, 
			#The -3 on the line above comes from the number of pages rounds before the task begins, so the instructions_quiz_page, etc. don't count as missed problems.
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,
			'int0' : m[0],
			'int1' : m[1],
			'int2' : m[2],
			'int3' : m[3],
			'int4' : m[4],
			'int5' : m[5],
			'int6' : m[6],
			'int7' : m[7],
			'int8' : m[8],
			'int9' : m[9],
			'int10' : m[10],
			'int11' : m[11],
			'int12' : m[12],
			'int13' : m[13],
			'int14' : m[14],
			'int15' : m[15],
			'int16' : m[16],
			'int17' : m[17],
			'int18' : m[18],
			'int19' : m[19],
			'int20' : m[20],
			'int21' : m[21],
			'int22' : m[22],
			'int23' : m[23],
			'int24' : m[24],
			'solution' : self.solution
		}

				
	def before_next_page(self):
		self.player.score_round_second_task(self.solution) #Need to write a score_round function for second task.
		self.solution=0
		if(self.participant.vars['out_of_time_second_task'] - time.time() < 0):
			self.participant.vars['show_feed_back_page'] = True
		
	
		
	
	
class feedback_page(Page):


	def is_displayed(self):
		return self.participant.vars['show_feed_back_page']
		
	def before_next_page(self):
		self.participant.vars['show_results_page_next'] = True
		self.participant.vars['show_first_task_page_next'] = False
		self.participant.vars['show_feed_back_page'] = False

		
		
class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		pass


class Results(Page):
	def is_displayed(self):
		return self.participant.vars['show_results_page_next']
		
	def vars_for_template(self):

		total_payoff_first_task = 0
		total_payoff_second_task = 0
		total_probs_attempted_task_one = 0
		total_probs_attempted_task_two = 0
		for p in self.player.in_all_rounds():
			if p.first_payoff_score != None: 
				total_payoff_first_task += p.first_payoff_score
			if p.second_payoff_score != None:
				total_payoff_second_task += p.second_payoff_score
			if p.problems_attempted_first_task != None:
				total_probs_attempted_task_one += p.problems_attempted_first_task
			if p.problems_attempted_second_task != None:
				total_probs_attempted_task_two += p.problems_attempted_second_task
				

		self.participant.vars['task_1_score'] = total_payoff_first_task
		self.participant.vars['task_2_score'] = total_payoff_second_task
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
						'payoff': round(prev_player.first_payoff_score),"""
                        'is_correct':prev_player.is_correct,
                        
                    }
					table_rows.append(row)

		self.participant.vars['t1_results'] = table_rows

		return {
		'table_rows': table_rows,
		'total_payoff_first_task':total_payoff_first_task,
		'problems_attempted_first_task': total_probs_attempted_task_one,
		'total_payoff_second_task':total_payoff_second_task,
		'problems_attempted_second_task':total_probs_attempted_task_two
		}
		


page_sequence = [
	start_page,
	instructions_quiz_page,
	first_task_page,
	message_page,
	investment_page,
	second_task_page,
	feedback_page,
	Results
]
