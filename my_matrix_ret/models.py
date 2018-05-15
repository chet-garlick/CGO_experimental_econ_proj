from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random 




author = 'Chet Garlick'

doc = """
Implementation of a real effort task that asks users to count to number of 1's and 0's in a 5x5 matrix of 1's and 0's.
"""


class Constants(BaseConstants):
    name_in_url = 'my_matrix_ret'
	task_timer = 120 #This is set to two minutes to make testing easier, this will probably be changed to 20 minutes (1200 seconds) for the real experiment.
    players_per_group = None
    num_rounds = 100 #Some number sufficiently high such that no one can solve this many matrices in the total time alloted (see task_timer)


class Subsession(BaseSubsession):
    #TODO:: Write stuff in here intializing int1-in25 correctly and finding the solution.
	#How can we randomize the matrix each round? Will a simple call to a random number generator work?
	
	def creating_session(self):
		players = self.get_players()
        if 'task_timer' in self.session.config:
            task_timer = self.session.config['task_timer']
        else:
            task_timer = Constants.task_timer
		for p in self.get_players():
			init_player_data(p)
        
	def init_player_data(p):
		p.task_timer = task_timer
		m = []
		for i in range(0,24):
		#This for loop adds 25 random ints that are either 0 or 1 into the array m.
		#The solution is incremented by whatever the random integer was, so that p.solution will correctly track the number of ones in m.
			x = random.randint(0,1)
			m.append(x)
			p.solution += x		
			
			
		p.int1 = m[1]
		p.int2 = m[2]
		p.int3 = m[3]
		p.int4 = m[4]
		p.int5 = m[5]
		p.int6 = m[6]
		p.int7 = m[7]
		p.int8 = m[8]
		p.int9 = m[9]
		p.int10 =m[10]
		p.int11 =m[11]
		p.int12 =m[12]
		p.int13 =m[13]
		p.int14 =m[14]
		p.int15 =m[15]
		p.int16 =m[16]
		p.int17 =m[17]
		p.int18 =m[18]
		p.int19 =m[19]
		p.int20 =m[20]
		p.int21 =m[21]
		p.int22 =m[22]
		p.int23 =m[23]
		p.int24 =m[24]
		p.int25 =m[25]



class Group(BaseGroup):
    pass #I don't think I need anything here, because it is not a multi-player game.


class Player(BasePlayer):
	def score_round(self):
		if(self.user_total == self.solution): #If the subject gets the correct answer, give them a point for the answer.
			self.is_correct = True
			self.payoff_score=1
		else:
			self_is_correct = False
			self.payoff_score=c(0)
			
			
			
			
	task_timer = models.PositiveIntegerField(
        doc="""The length of the real effort task timer."""
    )
	
    solution = models.PositiveIntegerField(
        doc="this round's correct solution")

    user_total = models.PositiveIntegerField(
        min = 0,
        max = 100,
        doc="user's summation",
        widget=widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

    payoff_score = models.FloatField(
            doc = '''score in this task'''
        )	

		
	int1 = models.PositiveIntegerField(
        doc="the matrix for this round's 1st entry")

    int2 = models.PositiveIntegerField(
        doc="the matrix for this round's 2nd entry")
		
	int3 = models.PositiveIntegerField(
        doc="the matrix for this round's 3rd entry")
		
	int4 = models.PositiveIntegerField(
        doc="the matrix for this round's 4th entry")
		
	int5 = models.PositiveIntegerField(
        doc="the matrix for this round's 5th entry")
		
	int6 = models.PositiveIntegerField(
        doc="the matrix for this round's 6th entry")
		
	int7 = models.PositiveIntegerField(
        doc="the matrix for this round's 7th entry")
		
	int8 = models.PositiveIntegerField(
        doc="the matrix for this round's 8th entry")
		
	int9 = models.PositiveIntegerField(
        doc="the matrix for this round's 9th entry")
		
	int10 = models.PositiveIntegerField(
        doc="the matrix for this round's 10th entry")
		
	int11 = models.PositiveIntegerField(
        doc="the matrix for this round's 11th entry")
		
	int12 = models.PositiveIntegerField(
        doc="the matrix for this round's 12th entry")
		
	int13 = models.PositiveIntegerField(
        doc="the matrix for this round's 13th entry")

	int14 = models.PositiveIntegerField(
        doc="the matrix for this round's 14th entry")

	int15 = models.PositiveIntegerField(
        doc="the matrix for this round's 15th entry")
		
	int16 = models.PositiveIntegerField(
        doc="the matrix for this round's 16th entry")
		
	int17 = models.PositiveIntegerField(
        doc="the matrix for this round's 17th entry")
		
	int18 = models.PositiveIntegerField(
        doc="the matrix for this round's 18th entry")
		
	int19 = models.PositiveIntegerField(
        doc="the matrix for this round's 19th entry")
		
	int20 = models.PositiveIntegerField(
        doc="the matrix for this round's 20th entry")
		
	int21 = models.PositiveIntegerField(
        doc="the matrix for this round's 21st entry")
		
	int22 = models.PositiveIntegerField(
        doc="the matrix for this round's 22nd entry")
		
	int23 = models.PositiveIntegerField(
        doc="the matrix for this round's 23rd entry")
		
	int24 = models.PositiveIntegerField{
		doc="the matrix for this round's 24th entry")
	
	int25 = models.PositiveIntegerField{
		doc="the matrix for this round's 25th entry")
		