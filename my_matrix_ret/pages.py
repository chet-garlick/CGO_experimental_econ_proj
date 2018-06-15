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
	
		"""
		Note about self.participant.vars: It is a python dictionary, which means it can store basically any type of data, and is accessed by a key.
		Additionally, each participant has a dictionary assigned to them that can be accessed at any time by any of the pages they are on. 
		This is a well designed feature by OTree, as it allows us to keep track of relevant data.
		Each participant gets a random set of 1's/0's and corresponding solution.
		By defining most of the self.participant.vars entries here in start_page's before_next_page, it is gauranteed that they will be accessible everywhere.
		This is because every participant goes through the start page before anything else happens, so we can initialize important stuff here.
		"""
		self.participant.vars['show_first_task_page_next'] = False
		self.participant.vars['out_of_time_first_task'] = 0
		self.participant.vars['show_message_page_next'] = False
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = False
		self.participant.vars['show_results_page_next'] = False
		self.participant.vars['show_feed_back_page'] = False
		self.participant.vars['out_of_time_second_task'] = 0
		
		
		
		#Using this section as a way to store the random integers and solution so that they are unique to each player.
		#If this works, then they don't need to be in models.py and won't show up as unecessary extra information in the data export.
		#UPDATE: This works perfect.
		list = []
		tmpsolution=0
		for i in range (0,25):
			tmp= random.randint(0,1)
			list.append(tmp)
			tmpsolution += tmp
			
		self.participant.vars['int_list'] = list
		self.participant.vars['solution'] = tmpsolution
		self.participant.vars['problems_attempted_first_task'] = 0
		self.participant.vars['problems_attempted_second_task'] = 0
		self.participant.vars['problems_correct_first_task'] = 0
		self.participant.vars['problems_correct_second_task'] = 0
		#print(self.participant.vars['int_list'])
		#print(self.participant.vars['solution'])
	def vars_for_template(self):
		return {
			'debug': settings.DEBUG,  
		}

class instructions_quiz_page(Page):
	def is_displayed(self):
		return self.round_number == 2
		
	def before_next_page(self):
		self.participant.vars['out_of_time_first_task'] = time.time() + Constants.first_task_timer
		self.participant.vars['show_first_task_page_next'] = True
			
		
		
		
class first_task_page(Page):
	form_model = models.Player
	form_fields = ['user_input']
	timer_text = 'Time left to solve problems:'
	#solution=0
	#solution=self.participant.vars['solution']
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_first_task'] - time.time()
		
	def is_displayed(self):
		return (self.participant.vars['out_of_time_first_task'] - time.time() > 0 and self.participant.vars['show_first_task_page_next'])
		#The line above returns true if the statements on either side of the 'and' operator return true. 
		#This means that the is_displayed funtion will only return true (and display this page) if self.round_number is greater than two and there is still time left on the first timer.
		
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		ints = self.participant.vars['int_list']
		#self.solution = self.participant.vars['solution']
		total_payoff = 0
		#num_attempted = 0
		
		for p in self.player.in_all_rounds(): #This loops over every round and totals the payoff scores for each player.
			if p.round_attempted: 
				p.problems_attempted_first_task = self.participant.vars['problems_attempted_first_task']
				p.problems_correct_first_task = self.participant.vars['problems_correct_first_task']
				
			if self.participant.vars['problems_attempted_first_task']==0: #on very first task dont display the correctness of previous answer.
					correct_last_round = "<br>"
			else: #all subsequent tasks display the correctness of previous answer.
				#using num_attemped as a helper variable so that on the first attempt the user won't see "correctly answered 0 out of None"
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'problems_attempted_first_task':round(self.participant.vars['problems_attempted_first_task']), 
			'num_correct_first_task': round(self.participant.vars['problems_correct_first_task']),
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,
			'int0' : ints[0],
			'int1' : ints[1],
			'int2' : ints[2],
			'int3' : ints[3],
			'int4' : ints[4],
			'int5' : ints[5],
			'int6' : ints[6],
			'int7' : ints[7],
			'int8' : ints[8],
			'int9' : ints[9],
			'int10' : 	ints[10],
			'int11' : 	ints[11],
			'int12' : 	ints[12],
			'int13' : 	ints[13],
			'int14' : 	ints[14],
			'int15' : 	ints[15],
			'int16' : 	ints[16],
			'int17' : 	ints[17],
			'int18' : 	ints[18],
			'int19' : 	ints[19],
			'int20' : 	ints[20],
			'int21' : 	ints[21],
			'int22' : 	ints[22],
			'int23' : 	ints[23],
			'int24' : 	ints[24],
			'solution' : self.participant.vars['solution']
		}

				
	def before_next_page(self):
		if self.player.user_input == self.participant.vars['solution']:
			self.player.score_round(True)
			self.participant.vars['problems_correct_first_task']+=1
			#print("correct! solution was: ", self.participant.vars['solution'], "you inputted: ", self.player.user_input)
		else: 
			self.player.score_round(False)
			#print("incorrect... solution was: ",self.participant.vars['solution'], "you inputted: ", self.player.user_input)
			
		#The section below recreates a list of 25 0's and 1's, sums them up, then saves them to self.participant.vars. 
		#This allows us to re-randomize a problem and solution after one is solved.
		#This is done every time this page is exited, rather than randomizing all problems for all rounds at once like it was doing when the randomization was in models.py.
		#This is going to be less resource intensive, which is not the primary reason I moved the randomization to pages.py but is an added benefit.
		new_ints=[]
		new_solution=0
		for i in range(0,25):
			tmp = random.randint(0,1)
			new_ints.append(tmp)
			new_solution += tmp
		
		self.participant.vars['int_list'] = new_ints
		self.participant.vars['solution'] = new_solution
		self.participant.vars['problems_attempted_first_task']+=1
		self.participant.vars['show_message_page_next']=True


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
		self.participant.vars['out_of_time_second_task'] = time.time() + Constants.second_task_timer
		
		
class second_task_page(Page):

	form_model = models.Player
	form_fields = ['user_input']	
	timer_text = 'Time left to solve problems:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_second_task'] - time.time()
	
	def is_displayed(self):
		return (self.participant.vars['show_second_task_next'] and (self.participant.vars['out_of_time_second_task'] - time.time() > 0))
	
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		ints = self.participant.vars['int_list']
		self.solution = self.participant.vars['solution']
		
		for p in self.player.in_all_rounds():
			if p.round_attempted: 
				p.problems_attempted_second_task = self.participant.vars['problems_attempted_first_task']
				p.problems_correct_second_task = self.participant.vars['problems_correct_second_task']

			if (self.participant.vars['problems_attempted_second_task']==0): 
					correct_last_round = "<br>"
			else: #all subsequent tasks displace the correctness of previous answer.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'problems_attempted_second_task':round(self.participant.vars['problems_attempted_second_task']), 
			'num_correct_second_task': round(self.participant.vars['problems_correct_second_task']),
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,
			'int0' : ints[0],
			'int1' : ints[1],
			'int2' : ints[2],
			'int3' : ints[3],
			'int4' : ints[4],
			'int5' : ints[5],
			'int6' : ints[6],
			'int7' : ints[7],
			'int8' : ints[8],
			'int9' : ints[9],
			'int10' : 	ints[10],
			'int11' : 	ints[11],
			'int12' : 	ints[12],
			'int13' : 	ints[13],
			'int14' : 	ints[14],
			'int15' : 	ints[15],
			'int16' : 	ints[16],
			'int17' : 	ints[17],
			'int18' : 	ints[18],
			'int19' : 	ints[19],
			'int20' : 	ints[20],
			'int21' : 	ints[21],
			'int22' : 	ints[22],
			'int23' : 	ints[23],
			'int24' : 	ints[24],
			'solution' : self.participant.vars['solution']
		}

				
	def before_next_page(self):
		if self.player.user_input == self.participant.vars['solution']:
			self.player.score_round_second_task(True)
			self.participant.vars['problems_correct_second_task']+=1
			#print("correct! solution was: ", self.participant.vars['solution'], "you inputted: ", self.player.user_input)
		else: 
			self.player.score_round_second_task(False)
			#print("incorrect... solution was: ",self.participant.vars['solution'], "you inputted: ", self.player.user_input)
		
		new_ints=[]
		new_solution=0
		for i in range(0,25):
			tmp = random.randint(0,1)
			new_ints.append(tmp)
			new_solution += tmp
		
		self.participant.vars['show_feed_back_page']=True
		self.participant.vars['int_list'] = new_ints
		self.participant.vars['solution'] = new_solution
		self.participant.vars['problems_attempted_second_task']+=1
		
	
class feedback_page(Page):


	def is_displayed(self):
		return (self.participant.vars['show_feed_back_page'] and (self.participant.vars['out_of_time_second_task']-time.time()<=0))
		
	def before_next_page(self):
		self.participant.vars['show_results_page_next'] = True
		#self.participant.vars['show_first_task_page_next'] = False
		self.participant.vars['show_feed_back_page'] = False

		
		
class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		pass


class Results(Page):
	def is_displayed(self):
		return self.participant.vars['show_results_page_next']
		
	def before_next_page(self):
		self.participant.vars['show_results_page_next'] = False
		
	def vars_for_template(self):
	
		return {
			'num_correct_first_task': round(self.participant.vars['problems_correct_first_task']),
			'problems_attempted_first_task': round(self.participant.vars['problems_attempted_first_task']),
			'num_correct_second_task': round(self.participant.vars['problems_correct_second_task']),
			'problems_attempted_second_task': round(self.participant.vars['problems_attempted_second_task']),
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
