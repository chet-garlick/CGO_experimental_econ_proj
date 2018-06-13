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
			solution=0 #variable containing corect solution for this counting exercise
			m=[] #list containing the list of integers used to populate the counting exercise 
			for i in range(0,25):
		#This for loop adds 25 random ints that are either 0 or 1 into the array m.
		
		for i in range(1,25): #for loop that randomly creates 25 ones and zeros then adding them to the list 'm'
			x = random.randint(0,1) #random.randint comes from python's built in random library, the arguments (0,1) tells randint to grab a random integer from the inclusive range (0,1)
				x = random.randint(0,1)
				m.append(x)
				solution += x #The solution is incremented by whatever the random integer was, so that p.solution will correctly track the number of ones in m.
					
			
			
			p.int1 = m[0]
			p.int2 = m[1]
			p.int3 = m[2]
			p.int4 = m[3]
			p.int5 = m[4]
			p.int6 = m[5]
			p.int7 = m[6]
			p.int8 = m[7]
			p.int9 = m[8]
			p.int10 =m[9]
			p.int11 =m[10]
			p.int12 =m[11]
			p.int13 =m[12]
			p.int14 =m[13]
			p.int15 =m[14]
			p.int16 =m[15]
			p.int17 =m[16]
			p.int18 =m[17]
			p.int19 =m[18]
			p.int20 =m[19]
			p.int21 =m[20]
			p.int22 =m[21]
			p.int23 =m[22]
			p.int24 =m[23]
			p.int25 =m[24]
			p.solution = solution
        

class Group(BaseGroup):
    pass #I don't think I need anything here, because it is not a multi-player game.


class Player(BasePlayer):
	def score_round(self):
		self.problems_attempted_first_task=1
		if(self.user_input == self.solution): #If the subject gets the correct answer, give them a point for the answer.
			self.is_correct = True
			self.first_payoff_score=1
		else:
			self_is_correct = False
			self.first_payoff_score=0
			
	def score_round_second_task(self):
		self.problems_attempted_second_task=1
		if(self.user_input == self.solution):
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
	"""
	ints = ['']
	for i in range(1,25):
		ints.append(0)
		
	int1 =0
	int2=0
	int4=0
	int5=0
	int6=0
	int7=0
	int8=0
	int9=0
	int10=0
	int11=0
	int12=0
	int13=0
	int14=0
	int15=0
	int16=0
	int17=0
	int18=0
	int19=0
	int20=0
	int21=0
	int22=0
	int23=0
	int24=0
	int25=0"""
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
		
	int24 = models.PositiveIntegerField(
		doc="the matrix for this round's 24th entry")
	
	int25 = models.PositiveIntegerField(
		doc="the matrix for this round's 25th entry")
		
		
		
		
		
