from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random 

author = 'Chet Garlick'

doc = "Implementation of a real effort task that asks users to count to number of 1's in a 5x5 matrix of 1's and 0's. This app also contains an Eckel/Grossman risk task, a Cognitive Reflection test, and a handful of survey questions."


class Constants(BaseConstants):

	participation_fee = c(1.0) #This is the aomunt user participant earns for showing up.
	first_task_payoff = c(1.0) #This is the flat amount each participant earns during the first section.
	card_message_correlation = 0.6 #This controls another one of the treatment variables, which affects the message that the user sees and how likely the message is to be correct.
	investment_cost = c(0.0) #This is the cost of investing to mitigate red-card losses.
	red_card_modifier = c(0.02) #This is the amount earned per answer if no investment is made and the participant has a red card.
	investment_effectiveness = c(0.10) #This is the amount earned per answer if the participant's card color is red and they chose to make the investment.
	#One treatment for the experiment is to set investment_effectiveness to c(.10) - which is 10 cents per correct question.
	#Another treatment for the experiment is to set it to c(0.05) - which is 5 cents per correct question.
	#This only affects payoffs if the participant's card is red and they chose to invest.
	green_card_payoff = c(0.15) #This is the amount earned per answer if the participant's card is green.
	first_task_timer = 20 #Length of first task - in seconds.
	second_task_timer = 20 #Length of second task - in seconds.
	message_version = 1 #This setting controls which version of the message page the participants will see. 
	#Setting it to 1 will give all users the option to choose whether or not they want the message.
	#Setting this to 2 will force all users to see the message.
	#Setting this to 3 will prevent all of the users from seeing the message at all.
	
	
	
	num_rounds = 100  #Some number sufficiently high such that no one can solve this many matrices in the total time alloted (see task_timer)
	name_in_url = 'my_matrix_ret'
	players_per_group = None



class Subsession(BaseSubsession):
	pass
class Group(BaseGroup):
    pass #I don't think I need anything here, because it is not a multi-player game.


class Player(BasePlayer):

	def score_round(self, correct_answer):
		self.round_attempted = True
		if correct_answer: #If the subject gets the correct answer, give them a point for the answer.
			self.is_correct = True
		else:
			self_is_correct = False
			
	def score_round_second_task(self, correct_answer):
		if(correct_answer):
			self.is_correct = True
		else:
			self_is_correct = False
			
	def determine_payoff(self):
		payoff=Constants.participation_fee
		payoff+=Constants.first_task_payoff
		if(self.card_color=='GREEN'):
			payoff+=Constants.green_card_payoff * self.problems_correct_second_task
		elif(self.card_color=='RED' and self.investment_choice):
			payoff+=Constants.investment_effectiveness * self.problems_correct_second_task
		else:
			payoff+=Constants.red_card_modifier * self.problems_correct_second_task
		if (self.investment_choice == True):
			payoff = payoff - Constants.investment_cost
			
		self.payoff = payoff

		
	total_payoff = models.FloatField(
		doc="The total dollar amount the participant earned by being a part of the experiment",
	)
	
	card_color = models.StringField(
		doc = "The color of the participant's card.",
		choices=['RED','GREEN'],
		initial='GREEN'
	)
	
	instructions_quiz_input1 = models.FloatField(
	)
	
	instructions_quiz_input2 = models.FloatField(
	)
	
	instructions_quiz_input3 = models.FloatField(
	)
	
	instructions_quiz_input4 = models.FloatField(
	)
	
	instructions_quiz_input5 = models.FloatField(
	)
	user_input = models.PositiveIntegerField(
		min = 0,
		max = 100,
		doc="user's summation",
		widget=widgets.TextInput(attrs={'autocomplete':'off'})
	)
	round_attempted = models.BooleanField(
		doc="Did the user attempt to answer this problem?",
		initial=False
	)
	
	is_correct = models.BooleanField(
        doc="did the user get the task correct?"
	)
	problems_attempted_first_task = models.PositiveIntegerField(
		doc="number of problems the user attempted"
	)
	problems_correct_first_task = models.PositiveIntegerField(
            doc = 'number of problems correctly solved in first task'
	)	
	problems_correct_second_task = models.PositiveIntegerField(
		doc="number of problems correctly solved in second task"
	)
	problems_attempted_second_task = models.PositiveIntegerField(
		doc="number of problems attempted in the second real effort task"
	)
	
	risk_choice = models.PositiveIntegerField(
		doc="Which choice the participant made in the Eckel/Grossman single choice list risk task.",
		choices=[1,2,3,4,5],
	)
	
	risk_payment=models.CurrencyField(
		doc = "Payment received for the participants risk choice."
	)
	
	message_page_version = models.PositiveIntegerField(
		doc = "Which version of the message page the participant views. If 1, the participant has the option to choose whether or not to see the message. If 2, the participant is forced to see the message. If 3, the user is forced to not see the message.",
		choices=[1,2,3],
	)
	
	message_choice = models.BooleanField(
		doc= "The choice of participants that have the option whether or not to see the message. For the other participants who don't have a choice, this will remain blank.",
		choices=[
		[True,'Yes'],[False,'No']
		],
		widget=widgets.RadioSelect
	)
	
	message_seen = models.BooleanField(
		doc="Was the message seen by the participant?"
	)
	
	investment_choice = models.BooleanField(
		doc="Did the participant decide to make the investment or not?",
		choices=[
		[True,'Yes'],
		[False,'No'],
		]
	)
	
	cog_reflect_one_input = models.FloatField(
		doc="User input for the first Cognitive Reflection Test Question.",
		min=0
	)
	
	cog_reflect_one_correct = models.BooleanField(
		doc="Did the user get the first Cognitive Reflection Test Question correct?"
	)
	
	cog_reflect_two_input = models.FloatField(
		doc="User input for the second Cognitive Reflection Test Question.",
		min=0
	)
	
	cog_reflect_two_correct = models.BooleanField(
		doc="Did the user get the second Cognitive Reflection Test Question correct?"
	)
	
	cog_reflect_three_input = models.FloatField(
		doc="User input for the third Cognitive Reflection Test Question.",
		min=0
	)
	
	cog_reflect_three_correct = models.BooleanField(
		doc="Did the user get the third Cognitive Reflection Test Question correct?"
	)
	
	gender = models.StringField(
		choices=['Male','Female','Prefer Not To Answer'],
		doc="Self-reported gender of the participant."
	)	
	
	major = models.StringField(
		doc = "Self-reported college major of the participant."
	)
	
	age = models.PositiveIntegerField(
		doc = "Self-reported age of participant.",
		min=0,
		max=100
	)
	
	ethnicity = models.StringField(
		doc = "Self-reported ethinicity of the participant.",
		choices = ['White','Hispanic or Latino', 'African American', 'Native American or American Indian', 'Asian', 'Pacific Islander', 'Other']
	)
	
	civil_status = models.StringField(
		doc = "Self-rerported civil status of participant.",
		choices=['Single, Never Married', 'Married/Domestic Partnership', 'Widowed', 'Divorced']		
	)
	
	employment = models.StringField(
		doc = "Employment status of participant.",
		choices = ['Yes','No']
	)
		
	insurance = models.StringField(
		doc = "Insured status of participant.",
		choices = ['Yes','No']
	)
	
	annual_income = models.FloatField(
		doc = "Self-reported household annual income of participant.",
		min = 0
	)
	
	credit_card = models.StringField(
		doc = "Does the participant have a credit card?",
		choices = ['Yes','No']
	)
	
	parent_education = models.StringField(
		doc =  "Highest level of education one of the parents of the participant completed.",
		choices = ['1st grade','2nd grade','3rd grade', '4th grade','5th grade','6th grade','7th grade',
		'8th grade', '9th grade', '10th grade', '11th grade', 'Graduated High School', '1 year of college', 
		'2 years of college','3 years of college', 'Graduated from college', 'Some graduate school', 'Completed graduate school']
	
	)
	
	smoke = models.StringField(
		doc = "Does the participant smoke?",
		choices = ['Yes','No']
	)
	
	alcohol = models.StringField(
		doc = "Does the participant drink alcohol?",
		choices = ['Yes','No']
	)
	
	year_in_school = models.StringField(
		doc = "What year of their college education is the participant currently in?",
		choices = ['Freshman','Sophomore','Junior','Senior', '5th year or more']
	)
	
	