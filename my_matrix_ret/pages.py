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
    version=request.GET.get('page_version')
    player = models.Player.objects.get(pk=id)
    if(version=="1"):
        player.problems_attempted_first_task+=1
        if(int(user_input)==int(solution)):
            player.problems_correct_first_task+=1
    elif(version=="2"):
        player.problems_attempted_second_task+=1
        if(int(user_input)==int(solution)):
            player.problems_correct_second_task+=1
        
    player.save()
    ints = []
    solution=0
    for i in range (0,25):
        tmp= random.randint(0,1)
        ints.append(tmp)
        solution += tmp
            
    earningsGREEN = Constants.green_card_payoff * player.problems_correct_second_task
    if(player.investment_choice): earningsRED = player.problems_correct_second_task * Constants.investment_effectiveness - Constants.investment_cost 
    else: earningsRED = player.problems_correct_second_task * Constants.red_card_modifier
    data = ({'ints':ints, 'solution':solution, 'num_correct_first_task':player.problems_correct_first_task, 'num_correct_second_task':player.problems_correct_second_task, 'red_card_modifier': Constants.red_card_modifier,'green_card_payoff':Constants.green_card_payoff, 'earningsGREEN':earningsGREEN, 'earningsRED':earningsRED })  
    return JsonResponse(data)

class start_page(Page):

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
        self.participant.vars['show_actual_message'] = False
        
        list = []
        tmpsolution=0
        for i in range (0,25):
            tmp= random.randint(0,1)
            list.append(tmp)
            tmpsolution += tmp
            
        self.participant.vars['int_list'] = list
        self.participant.vars['solution'] = tmpsolution
        self.player.set_card_color() #This line initialzes all of the red card participants according to the list of participants to be assigned red cards in the Constants section in models.py.
        
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,  
        }
        
class instructions_quiz_page(Page):
    form_model = 'player'
    form_fields=['instructions_quiz_input1','instructions_quiz_input2','instructions_quiz_input3','instructions_quiz_input4','instructions_quiz_input5']        
    def error_message(self,values):
        if( float(values['instructions_quiz_input1'])!=Constants.investment_effectiveness*37):
            return ("There was an issue with question one. Please try again.")
        if( float(values['instructions_quiz_input2'])!=Constants.green_card_payoff*37):
            return ("There was an issue with question two. Please try again.")
        if( float(values['instructions_quiz_input3'])!=Constants.red_card_modifier*37):
            return ("There was an issue with question three. Please try again.")
        if( float(values['instructions_quiz_input4'])!=Constants.message_correlation):
            return ("There was an issue with question four. Please try again.")
        if( float(values['instructions_quiz_input5'])!=Constants.red_card_modifier):
            return ("There was an issue with question five. Please try again.")
    
class waitpage(WaitPage):
    title_text = "Waiting"
    body_text = "Waiting for all participants to get to this point."
        
class transition_page_1(Page):
    
    def before_next_page(self):
        self.participant.vars['out_of_time_first_task'] = time.time() + Constants.first_task_timer  
    
class first_task_page(Page):
    form_model = 'player'
    timer_text = 'Time left to solve problems:'

    def get_timeout_seconds(self):
        return self.participant.vars['out_of_time_first_task'] - time.time()
        
    def vars_for_template(self):
        #Function defining some of necessary info for displaying this page.
        earningsGREEN = self.player.problems_correct_first_task * Constants.green_card_payoff
        earningsRED = self.player.problems_correct_first_task * Constants.red_card_modifier
        earningsREDinvest = self.player.problems_correct_first_task * Constants.investment_effectiveness
        ints = self.participant.vars['int_list']        
        
        return {
            'problems_attempted_first_task':round(self.player.problems_attempted_first_task), 
            'num_correct_first_task': round(self.player.problems_correct_first_task),
            'debug': settings.DEBUG,
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
            'version' : 1,
        }
                
    def before_next_page(self):
        new_ints=[]
        new_solution=0
        for i in range(0,25):
            tmp = random.randint(0,1)
            new_ints.append(tmp)
            new_solution += tmp
        self.participant.vars['int_list'] = new_ints
        self.participant.vars['solution'] = new_solution
        """
        This section recreates a list of 25 0's and 1's, sums them up, then saves them to self.participant.vars. 
        This allows us to re-randomize a problem and solution after one is solved.
        This is done every time this page is exited, rather than randomizing all problems for all rounds at once like it was doing when the randomization was in models.py.
        This is going to be less resource intensive, which is not the primary reason I moved the randomization to pages.py but is an added benefit.
        new_ints, new_solution, and tmp are temporary variables used to generate the next problem and solution.
        """

            
class transition_page_2(Page):

    def before_next_page(self):
        self.participant.vars['show_transition_2'] = False
        
    
class message_page_1(Page):
    form_model = 'player'
    form_fields = ['message_choice']
    def before_next_page(self):     
        if(self.player.message_choice==True):
            self.participant.vars['show_actual_message']=True
            self.player.message_seen = True
        elif(self.player.message_choice==False):
            self.player.message_seen = False
            
    def is_displayed(self):
        return Constants.message_version==1
    
    
class message_page_2(Page):
    def before_next_page(self):
        self.participant.vars['show_actual_message']=True
        for p in self.player.in_all_rounds():
            p.message_page_version = 2

    def is_displayed(self):
        return Constants.message_version==2

        
class message_page_3(Page):
    def before_next_page(self):
        for p in self.player.in_all_rounds():
            p.message_page_version = 3
            p.message_seen = False

    def is_displayed(self):
        return Constants.message_version==3
    
    
class message(Page):
    def is_displayed(self):
        return self.participant.vars['show_actual_message']
    
    def before_next_page(self):
        self.player.message_seen = True

    
class investment_page(Page):
    form_model = 'player'
    form_fields = ['investment_choice']
        
    def vars_for_template(self):
        
        return {
            'investment_cost' : Constants.investment_cost,
            'investment_effectiveness' : Constants.investment_effectiveness,
            'red_card_modifier' : Constants.red_card_modifier
        }
    
    
class transition_page_3(Page):
    def before_next_page(self):
        self.participant.vars['out_of_time_second_task'] = time.time() + Constants.second_task_timer    
    
class second_task_page(Page):

    form_model = 'player'   
    timer_text = 'Time left to solve problems:'
    
    def get_timeout_seconds(self):
        return self.participant.vars['out_of_time_second_task'] - time.time()
    
    def vars_for_template(self):
        #Function defining some of necessary info for displaying this page.
        ints = self.participant.vars['int_list']
        earningsGREEN = self.player.problems_correct_second_task * Constants.green_card_payoff
        if(self.player.investment_choice): earningsRED = self.player.problems_correct_second_task * Constants.investment_effectiveness
        else: earningsRED = self.player.problems_correct_second_task * Constants.red_card_modifier
        
        return {
            'problems_attempted_second_task':round(self.player.problems_attempted_second_task), 
            'num_correct_second_task': round(self.player.problems_correct_second_task),
            'num_correct_first_task': round(self.player.problems_correct_first_task),
            'debug': settings.DEBUG,
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
            'solution' : self.participant.vars['solution'],
            'version': 2,
            'id': self.player.pk,
        }

class transition_page_4(Page):

    form_model='player'
    form_fields=['inputted_card_color']
    def error_message(self,values):
        if(values['inputted_card_color']!=self.player.card_color):
            return ("That seems to be incorrect. Please try again.")
        
class Results(Page):
        
    def before_next_page(self):         
        self.player.determine_payoff()
        
    def vars_for_template(self):    
        if(self.player.card_color=='GREEN'): 
            second_task_earnings = self.player.problems_correct_second_task * Constants.green_card_payoff
        elif(self.player.card_color=='RED' and self.player.investment_choice):
            second_task_earnings = self.player.problems_correct_second_task * Constants.investment_effectiveness - Constants.investment_cost
        else:
            second_task_earnings = self.player.problems_correct_second_task * Constants.red_card_modifier
    
        return {
            'num_correct_first_task': round(self.player.problems_correct_first_task),
            'problems_attempted_first_task': round(self.player.problems_attempted_first_task),
            'num_correct_second_task': round(self.player.problems_correct_second_task),
            'problems_attempted_second_task': round(self.player.problems_attempted_second_task),
            'card_color' : self.player.card_color,
            'second_task_earnings': round(second_task_earnings,2),
            'first_task_payoff' : Constants.first_task_payoff,  
            'participation_fee' : Constants.participation_fee,          
        }
        
class transition_page_5(Page):
    pass
        
        
class risk_task(Page):

    form_model='player'
    form_fields=['risk_choice'] 
        
    def before_next_page(self):
        lottery_outcome = random.randint(0,1)
        self.player.risk_payment = self.participant.vars['lotteries'][self.player.risk_choice-1][lottery_outcome]
        self.player.payoff += self.player.risk_payment
            
    def vars_for_template(self):
        self.participant.vars['lotteries'] =  [[0]*2 for i in range(5)]
        self.participant.vars['lotteries'][0][0] = c(4.00)
        self.participant.vars['lotteries'][0][1] = c(4.00)
        self.participant.vars['lotteries'][1][0] = c(3.00)
        self.participant.vars['lotteries'][1][1] = c(6.00)
        self.participant.vars['lotteries'][2][0] = c(2.00)
        self.participant.vars['lotteries'][2][1] = c(8.00)
        self.participant.vars['lotteries'][3][0] = c(2.00)
        self.participant.vars['lotteries'][3][1] = c(10.00)
        self.participant.vars['lotteries'][4][0] = c(0.00)
        self.participant.vars['lotteries'][4][1] = c(12.00)
        
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
        
class transition_page_6(Page):
    pass
        
class cog_reflect_one(Page):

    form_model='player'
    form_fields=['cog_reflect_one_input']
        
    def before_next_page(self): 
        if(self.player.cog_reflect_one_input == .05):
            self.player.cog_reflect_one_correct = True
        else:
            self.player.cog_reflect_one_correct = False     
    
class cog_reflect_two(Page):
    form_model='player'
    form_fields=['cog_reflect_two_input']

    def before_next_page(self): 
        if(self.player.cog_reflect_two_input == 5):
            self.player.cog_reflect_two_correct = True
        else:
            self.player.cog_reflect_two_correct = False         
    
class cog_reflect_three(Page):
    form_model='player'
    form_fields=['cog_reflect_three_input']

    def before_next_page(self): 
        
        if(self.player.cog_reflect_three_input == 47):
            self.player.cog_reflect_three_correct = True
        else:
            self.player.cog_reflect_three_correct = False

            
class survey(Page):
    form_model='player'
    form_fields=['gender','major','age','ethnicity','marital_status','employment','insurance','annual_income',
    'credit_card','smoke','alcohol','parent_education','year_in_school']

    def vars_for_template(self):
        return{
            'debug' : settings.DEBUG
        }       
        
class finalPage(Page):
    pass
                
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
    transition_page_6,
    cog_reflect_one,
    cog_reflect_two,
    cog_reflect_three,
    survey,
    finalPage
]
