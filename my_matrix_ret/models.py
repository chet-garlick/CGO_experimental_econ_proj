from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random 




author = 'Chet Garlick'

doc = "Implementation of a real effort task that asks users to count to number of 1's in a 5x5 matrix of 1's and 0's."


class Constants(BaseConstants):
	name_in_url = 'my_matrix_ret'
	first_task_timer = 15
	second_task_timer = 15
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
			self.first_payoff_score=0
			
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
