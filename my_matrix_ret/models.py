from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random 




author = 'Chet Garlick'

doc = "Implementation of a real effort task that asks users to count to number of 1's in a 5x5 matrix of 1's and 0's."


class Constants(BaseConstants):
	name_in_url = 'my_matrix_ret'
	first_task_timer = 60
	second_task_timer = 30
	players_per_group = None
	num_rounds = 100
	#Some number sufficiently high such that no one can solve this many matrices in the total time alloted (see task_timer)


class Subsession(BaseSubsession):
    #TODO:: Write stuff in here intializing int1-in25 correctly and finding the solution.
	#How can we randomize the matrix each round? Will a simple call to a random number generator work?
	def creating_session(self):
		players = self.get_players()
		if 'first_task_timer' in self.session.config:
			first_task_timer = self.session.config['first_task_timer']
		else:
			first_task_timer = Constants.first_task_timer
		if 'second_task_timer' in self.session.config:
			second_task_timer = self.session.config['second_task_timer']
		else:
			second_task_timer = Constants.second_task_timer
		for p in self.get_players():
			p.first_task_timer = first_task_timer
			p.second_task_timer = second_task_timer
			

class Group(BaseGroup):
    pass #I don't think I need anything here, because it is not a multi-player game.


class Player(BasePlayer):
	def score_round(self, correct_answer):
		self.problems_attempted_first_task=1
		if correct_answer: #If the subject gets the correct answer, give them a point for the answer.
			self.is_correct = True
			self.first_payoff_score=1
		else:
			self_is_correct = False
			self.first_payoff_score=0
			
	def score_round_second_task(self, correct_answer):
		self.problems_attempted_second_task=1
		if(correct_answer):
			self.is_correct = True
			self.second_payoff_score=1
		else:
			self_is_correct = False
			self.second_payoff_score=0
			
			
			
			
	first_task_timer = models.PositiveIntegerField(
        doc="The length of the first real effort task timer."
    )
	
	second_task_timer = models.PositiveIntegerField(
        doc="The length of the second real effort task timer."
    )
	
	solution = models.PositiveIntegerField(
        doc="this round's correct solution"
	)

	user_input = models.PositiveIntegerField(
		min = 0,
		max = 100,
		doc="user's summation",
		widget=widgets.TextInput(attrs={'autocomplete':'off'})
	)

	is_correct = models.BooleanField(
        doc="did the user get the task correct?"
	)
	problems_attempted_first_task = models.PositiveIntegerField(
		doc="number of problems the user attempted"
	)
	first_payoff_score = models.FloatField(
            doc = 'number of problems correctly solved in first task'
	)	
	second_payoff_score = models.FloatField(
		doc="number of problems correctly solved in second task"
	)
	problems_attempted_second_task = models.PositiveIntegerField(
		doc="number of problems attempted in the second real effort task"
	)
		
		
		
		
