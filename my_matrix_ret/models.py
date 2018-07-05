from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random 

author = 'Chet Garlick'

doc = "Implementation of a real effort task that asks users to count to number of 1's in a 5x5 matrix of 1's and 0's. This app also contains an Eckel/Grossman risk task, a Cognitive Reflection test, and a handful of survey questions."


class Constants(BaseConstants):
	name_in_url = 'my_matrix_ret'
	first_task_timer = 3
	second_task_timer = 3
	players_per_group = None
	num_rounds = 100
	#Some number sufficiently high such that no one can solve this many matrices in the total time alloted (see task_timer)


class Subsession(BaseSubsession):
	pass
class Group(BaseGroup):
    pass #I don't think I need anything here, because it is not a multi-player game.


class Player(BasePlayer):
	def score_round(self, correct_answer):
		self.round_attempted=True
		if correct_answer: #If the subject gets the correct answer, give them a point for the answer.
			self.is_correct = True
		else:
			self_is_correct = False
			
	def score_round_second_task(self, correct_answer):
		if(correct_answer):
			self.is_correct = True
		else:
			self_is_correct = False

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
	
	message_choice = models.StringField(
		doc= "The choice of participants that have the option whether or not to see the message. For the other participants who don't have a choice, this will remain blank.",
		choices=['Yes','No'],
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
	
	