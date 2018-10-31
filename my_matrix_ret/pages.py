from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models
from django.conf import settings
import time
import random

from django.http import HttpResponse 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

	
@csrf_exempt
def verify(request):
	user_input = request.GET.get('user_input')
	solution = request.GET.get('s')
	id = request.GET.get('id')
	models.score_first_task(id,user_input,solution)
	#self.player.score_round_task1(user_input,solution)	
	data = ({'foo':'bar'})	
	return JsonResponse(data)

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
		self.participant.vars['out_of_time_first_task'] = 0
		self.participant.vars['out_of_time_second_task'] = 0
		self.participant.vars['show_first_task_page_next'] = False
		self.participant.vars['show_message_page_next'] = False
		self.participant.vars['show_actual_message'] = False
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = False
		self.participant.vars['show_results_page_next'] = False
		self.participant.vars['show_risk_task'] = False
		self.participant.vars['show_cog_reflect_one']= False
		self.participant.vars['show_cog_reflect_two']= False
		self.participant.vars['show_cog_reflect_three']= False
		self.participant.vars['show_survey_next'] = False
		self.participant.vars['show_wait_page'] = False
		self.participant.vars['show_final_page']=False
		self.participant.vars['show_instructions_quiz'] = True
		self.participant.vars['show_transition_1'] = False
		self.participant.vars['show_transition_2'] = False
		self.participant.vars['show_transition_3'] = False
		self.participant.vars['show_transition_4'] = False
		self.participant.vars['show_transition_5'] = False

		
		
		"""
		Additionally, I use boolean variables above in self.participant.vars as a way to gaurantee that pages are displayed in the correct order.
		Without these, the display logic with the timers can cause unpredictable sequencing.
		This is because OTree will look through the page_sequence and attempt to display anything it can. 
		On the pages with timers, is_displayed is necessary to ensure that they are displayed for the correct amount of time. Because of this,
		oTree will display anything without is_displayed logic before anything with is_displayed logic.
		To remedy this, I require all pages to have is_displayed logic in the form of a boolean variable in self.participant.vars.
		"""
		
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
		
		for p in self.player.in_all_rounds():
			p.set_card_color() #This line initialzes all of the red card participants according to the list of participants to be assigned red cards in the Constants section in models.py.
		
	def vars_for_template(self):
		return {
			'debug': settings.DEBUG,  
		}

		
class instructions_quiz_page(Page):
	form_model = 'player'
	form_fields=['instructions_quiz_input1','instructions_quiz_input2','instructions_quiz_input3','instructions_quiz_input4','instructions_quiz_input5']
	def is_displayed(self):
		return self.participant.vars['show_instructions_quiz']
		
	def before_next_page(self):

		self.participant.vars['show_wait_page'] = True
		self.participant.vars['show_transition_1'] = True
		self.participant.vars['show_instructions_quiz'] = False
		

class waitpage(WaitPage):
	title_text = "Waiting"
	body_text = "Waiting for all participants to get to this point."
	
	def is_displayed(self):
		return self.participant.vars['show_wait_page']
		
class transition_page_1(Page):
	def is_displayed(self):
		return self.participant.vars['show_transition_1']
	
	def before_next_page(self):
		self.participant.vars['out_of_time_first_task'] = time.time() + Constants.first_task_timer
		self.participant.vars['show_first_task_page_next'] = True
		self.participant.vars['show_transition_1'] = False
		self.participant.vars['show_wait_page'] = False
	
	
class first_task_page(Page):
	form_model = 'player'
	form_fields = ['user_input']
	timer_text = 'Time left to solve problems:'


	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_first_task'] - time.time()
		
	def is_displayed(self):
		return (self.participant.vars['out_of_time_first_task'] - time.time() > 0 and self.participant.vars['show_first_task_page_next'])
		#The line above returns true if the statements on either side of the 'and' operator return true. 
		#This means that the is_displayed funtion will only return true (and display this page) if self.round_number is greater than two and there is still time left on the first timer.
		
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		earningsGREEN = self.participant.vars['problems_correct_first_task'] * Constants.green_card_payoff
		earningsRED = self.participant.vars['problems_correct_first_task'] * Constants.red_card_modifier
		earningsREDinvest = self.participant.vars['problems_correct_first_task'] * Constants.investment_effectiveness
		ints = self.participant.vars['int_list']		
		for p in self.player.in_all_rounds(): #This loops over every round and totals the rounds attempted and correctly answered.
			if p.round_attempted: 
				p.problems_attempted_first_task = self.participant.vars['problems_attempted_first_task']
				p.problems_correct_first_task = self.participant.vars['problems_correct_first_task']
				
		
			if self.participant.vars['problems_attempted_first_task']==0: #on very first task dont display the correctness of previous answer.
			#correct_last_round is a string containing actual HTML that is being passed to the display. If no problems have been attempted this task, it is "<br>" which is HTML for a line break.
					correct_last_round = "<br>"
			else: #all subsequent tasks display the correctness of previous answer. The <font color= > </font> is HTML that colors the words correct/incorrect for a bit of flair.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'problems_attempted_first_task':round(self.participant.vars['problems_attempted_first_task']), 
			'num_correct_first_task': round(self.participant.vars['problems_correct_first_task']),
			'debug': settings.DEBUG,
			'correct_last_round': correct_last_round,
			'solution':self.participant.vars['solution'],
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
			'int10' : ints[10],
			'int11' : ints[11],
			'int12' : ints[12],
			'int13' : ints[13],
			'int14' : ints[14],
			'int15' : ints[15],
			'int16' : ints[16],
			'int17' : ints[17],
			'int18' : ints[18],
			'int19' : ints[19],
			'int20' : ints[20],
			'int21' : ints[21],
			'int22' : ints[22],
			'int23' : ints[23],
			'int24' : ints[24],
			'earningsGREEN' : earningsGREEN,
			'earningsRED' : earningsRED,
			'earningsREDinvest' : earningsREDinvest,
			'participation_fee' : Constants.participation_fee,
			'first_task_payoff' : Constants.first_task_payoff,
			'if_second_task_red_card' : earningsRED,
			'if_second_task_green_card' : earningsGREEN,
			'id' : self.player.pk,
		}
		
		

				
	def before_next_page(self):
		if self.player.user_input == self.participant.vars['solution']:
			self.player.score_round(True)
			self.participant.vars['problems_correct_first_task']+=1
		else: 
			self.player.score_round(False)
		"""
		The section below recreates a list of 25 0's and 1's, sums them up, then saves them to self.participant.vars. 
		This allows us to re-randomize a problem and solution after one is solved.
		This is done every time this page is exited, rather than randomizing all problems for all rounds at once like it was doing when the randomization was in models.py.
		This is going to be less resource intensive, which is not the primary reason I moved the randomization to pages.py but is an added benefit.
		new_ints, new_solution, and tmp are temporary variables used to generate the next problem and solution.
		"""
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
		if(self.participant.vars['out_of_time_first_task'] - time.time() <= 1):
			self.participant.vars['show_first_task_page_next'] = False
			self.participant.vars['show_transition_2'] = True
			self.participant.vars['show_wait_page'] = True

			
class transition_page_2(Page):
	def is_displayed(self):
			return self.participant.vars['show_transition_2']
	def before_next_page(self):
		self.participant.vars['show_transition_2'] = False
		
	
class message_page_1(Page):
	form_model = 'player'
	form_fields = ['message_choice']
	def before_next_page(self):
		self.participant.vars['show_message_page_next'] = False
		
		if(self.player.message_choice==True):
			self.participant.vars['show_actual_message']=True
		elif(self.player.message_choice==False):
			self.participant.vars['show_investment_page_next'] = True
			
		for p in self.player.in_all_rounds():
			p.message_page_version = 1
			p.message_choice = self.player.message_choice
			if(self.player.message_choice=='No'):
				p.message_seen = False
			
	def is_displayed(self):
		return self.participant.vars['out_of_time_first_task'] - time.time() < 0 and self.participant.vars['show_message_page_next'] and Constants.message_version==1
	
	
class message_page_2(Page):
	def before_next_page(self):
		self.participant.vars['show_message_page_next'] = False
		self.participant.vars['show_actual_message']=True
		for p in self.player.in_all_rounds():
			p.message_page_version = 2

	def is_displayed(self):
		return self.participant.vars['out_of_time_first_task'] - time.time() < 0 and self.participant.vars['show_message_page_next'] and Constants.message_version==2

		
class message_page_3(Page):
	def before_next_page(self):
		self.participant.vars['show_message_page_next'] = False
		self.participant.vars['show_investment_page_next'] = True
		for p in self.player.in_all_rounds():
			p.message_page_version = 3
			p.message_seen = False

	def is_displayed(self):
		return self.participant.vars['out_of_time_first_task'] - time.time() < 0 and self.participant.vars['show_message_page_next'] and Constants.message_version==3
	
	
class message(Page):
	def is_displayed(self):
		return self.participant.vars['show_actual_message']
	
	def before_next_page(self):
		self.participant.vars['show_investment_page_next'] = True
		self.participant.vars['show_actual_message']=False
		self.player.message_seen = True
		for p in self.player.in_all_rounds():
			p.message_seen = True

	
class investment_page(Page):
	
	form_model = 'player'
	form_fields = ['investment_choice']

	def is_displayed(self):
		return self.participant.vars['show_investment_page_next']

	def before_next_page(self):
		self.participant.vars['show_investment_page_next'] = False
		self.participant.vars['show_second_task_next'] = True
		self.participant.vars['show_transition_3'] = True
		self.participant.vars['out_of_time_second_task'] = time.time() + Constants.second_task_timer	
		for p in self.player.in_all_rounds():
			p.investment_choice = self.player.investment_choice
		
		
	def vars_for_template(self):
		
		return {
			'investment_cost' : Constants.investment_cost,
			'investment_effectiveness' : Constants.investment_effectiveness,
			'red_card_modifier' : Constants.red_card_modifier
		}
	
	
class transition_page_3(Page):
	def is_displayed(self):
		return self.participant.vars['show_transition_3']
	def before_next_page(self):
		self.participant.vars['show_transition_3'] = False
	
class second_task_page(Page):

	form_model = 'player'
	form_fields = ['user_input']	
	timer_text = 'Time left to solve problems:'
	
	def get_timeout_seconds(self):
		return self.participant.vars['out_of_time_second_task'] - time.time()
	
	def is_displayed(self):
		return (self.participant.vars['show_second_task_next'] and (self.participant.vars['out_of_time_second_task'] - time.time() > 0))
	
	def vars_for_template(self):
		#Function defining some of necessary info for displaying this page.
		ints = self.participant.vars['int_list']
		earningsGREEN = self.participant.vars['problems_correct_second_task'] * Constants.green_card_payoff
		if(self.player.investment_choice): earningsRED = self.participant.vars['problems_correct_second_task'] * Constants.investment_effectiveness
		else: earningsRED = self.participant.vars['problems_correct_second_task'] * Constants.red_card_modifier
		
		for p in self.player.in_all_rounds():
			if p.round_attempted: 
				p.problems_attempted_second_task = self.participant.vars['problems_attempted_second_task']
				p.problems_correct_second_task = self.participant.vars['problems_correct_second_task']

			if (self.participant.vars['problems_attempted_second_task']==0): 
			#correct_last_round is a string containing actual HTML that is being passed to the display.
			#If no problems have been attempted this task, it is "<br>" which is HTML for a line break.
				correct_last_round = "<br>"
			else: #all subsequent tasks display the correctness of previous answer.
				if self.player.in_previous_rounds()[-1].is_correct:
					correct_last_round = "Your last answer was <font color='green'>correct</font>"
				else: 
					correct_last_round = "Your last answer was <font color='red'>incorrect</font>"
        
		return {
			'problems_attempted_second_task':round(self.participant.vars['problems_attempted_second_task']), 
			'num_correct_second_task': round(self.participant.vars['problems_correct_second_task']),
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
			'int10' : ints[10],
			'int11' : ints[11],
			'int12' : ints[12],
			'int13' : ints[13],
			'int14' : ints[14],
			'int15' : ints[15],
			'int16' : ints[16],
			'int17' : ints[17],
			'int18' : ints[18],
			'int19' : ints[19],
			'int20' : ints[20],
			'int21' : ints[21],
			'int22' : ints[22],
			'int23' : ints[23],
			'int24' : ints[24],
			'earningsGREEN' : earningsGREEN,
			'earningsRED' : earningsRED,
			'first_task_payoff': Constants.first_task_payoff,
			'participation_fee': Constants.participation_fee,
		}
				
	def before_next_page(self):
		if self.player.user_input == self.participant.vars['solution']:
			self.player.score_round_second_task(True)
			self.participant.vars['problems_correct_second_task']+=1
		else: 
			self.player.score_round_second_task(False)
		
		new_ints=[]
		new_solution=0
		for i in range(0,25):
			tmp = random.randint(0,1)
			new_ints.append(tmp)
			new_solution += tmp
		
		self.participant.vars['show_results_page_next']=True
		self.participant.vars['int_list'] = new_ints
		self.participant.vars['solution'] = new_solution
		self.participant.vars['problems_attempted_second_task']+=1
		
		if(self.participant.vars['out_of_time_second_task'] - time.time()<=0):
			self.participant.vars['show_transition_4'] = True

class transition_page_4(Page):
	def is_displayed(self):
		return self.participant.vars['show_transition_4']
	def before_next_page(self):
		self.participant.vars['show_transition_4'] = False	
		
class Results(Page):
	def is_displayed(self):
		return (self.participant.vars['show_results_page_next'] and (self.participant.vars['out_of_time_second_task']-time.time()<=0))
		
	def before_next_page(self):
		self.participant.vars['show_results_page_next'] = False
		self.participant.vars['show_transition_5'] = True
		self.participant.vars['show_risk_task'] = True
		for p in self.player.in_all_rounds():
			p.problems_attempted_first_task = self.participant.vars['problems_attempted_first_task']
			p.problems_attempted_second_task = self.participant.vars['problems_attempted_second_task']
			p.problems_correct_first_task = self.participant.vars['problems_correct_first_task']
			p.problems_correct_second_task = self.participant.vars['problems_correct_second_task']
			
		self.player.determine_payoff()
		
	def vars_for_template(self):
		earningsGREEN = self.participant.vars['problems_correct_second_task']
		
		
		
		if(self.player.card_color=='GREEN'): 
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.green_card_payoff
		elif(self.player.card_color=='RED' and self.player.investment_choice):
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.investment_effectiveness - Constants.investment_cost
		else:
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.red_card_modifier

	
		return {
			'num_correct_first_task': round(self.participant.vars['problems_correct_first_task']),
			'problems_attempted_first_task': round(self.participant.vars['problems_attempted_first_task']),
			'num_correct_second_task': round(self.participant.vars['problems_correct_second_task']),
			'problems_attempted_second_task': round(self.participant.vars['problems_attempted_second_task']),
			'card_color' : self.player.card_color,
			'second_task_earnings': second_task_earnings,
			'first_task_payoff' : Constants.first_task_payoff,	
			'participation_fee' : Constants.participation_fee,			
		}
		
class transition_page_5(Page):
	def is_displayed(self):
		return self.participant.vars['show_transition_5']
		
	def before_next_page(self):
		self.participant.vars['show_transition_5'] = False
		
		
class risk_task(Page):

	form_model='player'
	form_fields=['risk_choice']
	
	def is_displayed(self):
		return self.participant.vars['show_risk_task']
		
		
	def before_next_page(self):
		self.participant.vars['show_risk_task'] = False
		self.participant.vars['show_cog_reflect_one'] = True
		lottery_outcome = random.randint(0,1)
		
		for p in self.player.in_all_rounds():
			p.risk_choice = self.player.risk_choice
			p.risk_payment = self.participant.vars['lotteries'][p.risk_choice-1][lottery_outcome]
			
			
	def vars_for_template(self):
		self.participant.vars['lotteries'] =  [[0]*2 for i in range(5)]

		self.participant.vars['lotteries'][0][0] = c(16.00)
		self.participant.vars['lotteries'][0][1] = c(16.00)
		self.participant.vars['lotteries'][1][0] = c(12.00)
		self.participant.vars['lotteries'][1][1] = c(24.00)
		self.participant.vars['lotteries'][2][0] = c(8.00)
		self.participant.vars['lotteries'][2][1] = c(32.00)
		self.participant.vars['lotteries'][3][0] = c(4.00)
		self.participant.vars['lotteries'][3][1] = c(40.00)
		self.participant.vars['lotteries'][4][0] = c(0.00)
		self.participant.vars['lotteries'][4][1] = c(48.00)
		
		
		return{
		 'option1A':self.participant.vars['lotteries'][0][0],
		 'option1B':self.participant.vars['lotteries'][0][1],
		 'option2A':self.participant.vars['lotteries'][1][0],
		 'option2B':self.participant.vars['lotteries'][1][1],
		 'option3A':self.participant.vars['lotteries'][2][0],
		 'option3B':self.participant.vars['lotteries'][2][1],
		 'option4A':self.participant.vars['lotteries'][3][0],
		 'option4B':self.participant.vars['lotteries'][3][1],
		 'option5A':self.participant.vars['lotteries'][4][0],
		 'option5B':self.participant.vars['lotteries'][4][1]		
		}
			
		
class cog_reflect_one(Page):

	form_model='player'
	form_fields=['cog_reflect_one_input']
	
	def is_displayed(self):
		return self.participant.vars['show_cog_reflect_one']
		
	def before_next_page(self):	
		
		self.participant.vars['show_cog_reflect_one'] = False
		self.participant.vars['show_cog_reflect_two'] = True
		if(self.player.cog_reflect_one_input == .05):
			self.player.cog_reflect_one_correct = True
		else:
			self.player.cog_reflect_one_correct = False		
		for p in self.player.in_all_rounds():
			p.cog_reflect_one_correct = self.player.cog_reflect_one_correct
	
	
class cog_reflect_two(Page):
	form_model='player'
	form_fields=['cog_reflect_two_input']
	def is_displayed(self):
		return self.participant.vars['show_cog_reflect_two']
	def before_next_page(self):	
		
		self.participant.vars['show_cog_reflect_two'] = False
		self.participant.vars['show_cog_reflect_three'] = True
		if(self.player.cog_reflect_two_input == 5):
			self.player.cog_reflect_two_correct = True
		else:
			self.player.cog_reflect_two_correct = False		
			
		for p in self.player.in_all_rounds():
			p.cog_reflect_two_correct = self.player.cog_reflect_two_correct
	
	
class cog_reflect_three(Page):
	form_model='player'
	form_fields=['cog_reflect_three_input']
	def is_displayed(self):
		return self.participant.vars['show_cog_reflect_three']
	def before_next_page(self):	
		self.participant.vars['show_cog_reflect_three'] = False
		self.participant.vars['show_survey_next'] = True
		
		if(self.player.cog_reflect_three_input == 47):
			self.player.cog_reflect_three_correct = True
		else:
			self.player.cog_reflect_three_correct = False
			
		for p in self.player.in_all_rounds():
			p.cog_reflect_three_correct = self.player.cog_reflect_three_correct

			
class survey(Page):
	form_model='player'
	form_fields=['gender','major','age','ethnicity','civil_status','employment','insurance','annual_income',
	'credit_card','smoke','alcohol','parent_education','year_in_school']
	def is_displayed(self):
		return self.participant.vars['show_survey_next']
	def vars_for_template(self):
		return{
			'debug' : settings.DEBUG
		}
	def before_next_page(self):
		self.participant.vars['show_final_page']=True
		#This section takes the values from the survey and updates every round with these values, hopefully making the data look a little cleaner.
		self.participant.vars['show_survey_next'] = False
		for p in self.player.in_all_rounds():
			p.gender = self.player.gender
			p.major = self.player.major
			p.age = self.player.age
			p.ethnicity = self.player.ethnicity
			p.civil_status = self.player.civil_status
			p.employment = self.player.employment
			p.insurance = self.player.insurance
			p.annual_income = self.player.annual_income
			p.credit_card = self.player.credit_card
			p.smoke = self.player.smoke
			p.alcohol = self.player.alcohol
			p.parent_education = self.player.parent_education
			p.year_in_school = self.player.year_in_school
			print(self.participant.payoff)

		
		
class finalPage(Page):
	def is_displayed(self):
		return self.participant.vars['show_final_page']
		
	def vars_for_template(self):
		earningsGREEN = self.participant.vars['problems_correct_second_task']
		if(self.player.card_color=='GREEN'): 
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.green_card_payoff
		elif(self.player.card_color=='RED' and self.player.investment_choice):
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.investment_effectiveness - Constants.investment_cost
		else:
			second_task_earnings = self.participant.vars['problems_correct_second_task'] * Constants.red_card_modifier

	
		return {
			'num_correct_first_task': round(self.participant.vars['problems_correct_first_task']),
			'problems_attempted_first_task': round(self.participant.vars['problems_attempted_first_task']),
			'num_correct_second_task': round(self.participant.vars['problems_correct_second_task']),
			'problems_attempted_second_task': round(self.participant.vars['problems_attempted_second_task']),
			'card_color' : self.player.card_color,
			'second_task_earnings': second_task_earnings,
			'first_task_payoff' : Constants.first_task_payoff,	
			'participation_fee' : Constants.participation_fee,
		}
			
		
page_sequence = [
	start_page,
	instructions_quiz_page,
	waitpage,
	transition_page_1,
	first_task_page,
	waitpage,
	transition_page_2,
	message_page_1,
	message_page_2,
	message_page_3,
	message,
	investment_page,
	waitpage,
	transition_page_3,
	second_task_page,
	waitpage,
	transition_page_4,
	Results,
	waitpage,
	transition_page_5,
	risk_task,
	cog_reflect_one,
	cog_reflect_two,
	cog_reflect_three,
	survey,
	finalPage
]
