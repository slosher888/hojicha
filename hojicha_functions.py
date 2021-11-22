#hojicha_functions.py

import random
import humanize
import datetime as dt
import requests

def draw_a_tarot_card(msg_args):
	response=requests.get('https://rws-cards-api.herokuapp.com/api/v1/cards/random?n=1').json()
	card=response['cards'][0]
	orientation=' '+random.choice(['right side up.','upside down.'])

	result='You have drawn '+ card['name']+orientation+'\n'
	result +='\nMeaning up:\n'
	result += card['meaning_up']
	result +='\n\nMeaning upside down:\n'
	result += card['meaning_rev']
	return result


def help_text():
	string=   'Hiii, I know the following commands:\n'
	string += 'SPEAK:    Give words of wisdom (a la fortune)\n'
	string += 'PICK:     Select from comma seperated list\n'
	string += 'Q <yes/no question>: Answer yes/no question\n'
	string += 'DRAW CARD <open ended question>: Gives single tarot card reading\n'
	string += 'UPTIME:   Tells you how long I have been awake B^]\n'
	string += 'ROLL NdM <+/-X>: M-sided die N times (optional +/- modifier)\n'
	string += 'HELP:     Display this message, obvs\n'
	return string

def pick_one(string):
	list=string.split(',')
	if list[0]=='':
		result = 'Umm..'
	elif len(list)==1:
		result = 'You gave me no choice, I pick ' + list[0] + '\nT_T'
	else:
		selection=random.choice(list)
		result = "I pick... " + selection
	return result

def yes_no(mesg):

		conviction=random.randint(0,10)
		modifier=''
		action=''

		if conviction == 5:
			return('Hojicha does not seem that interested in answering right now.')
		if conviction >= 0 and conviction <= 2:
			modifier=' a bit'
		if conviction > 2 and conviction <= 7:
			modifier=''
		if conviction > 7:
			modifier=' emphatically'
		answer=bool(random.randint(0,1))
		if answer:
			action='nods'
		else:
			action='shakes its head'
		reaction='Hojicha {act}{mod}.'.format(act=action,mod=modifier)
		original_question=' '.join(mesg.split(' ')[1:])
		response=reaction+'\n> Original question: '+original_question
		return response
def hojicha_uptime(wakeup_time):
	return humanize.naturaltime(dt.datetime.now()-wakeup_time)[:-4]+'.'

def roll_dice(msg_args):
# roll N dice with M sides with +/- K bonus/penalty
# format !hojicha roll NdM +/-K
	roll_args=msg_args.split(' ')
	dice_text=roll_args[2]
	[n,m] = dice_text.split('D')
	
		
	try:
		n=int(n)
		m=int(m)
	except ValueError:
		return 'Hojicha sniffs the wind...'
	if n > 800:
		return 'Hojicha doesn\'t really feel like doing that'
	dice_results=[ random.randint(1,m) for i in range(n)]	

	try:
		mod_text=roll_args[3]
		mod=int(mod_text[1:])
	except IndexError:
		result_string=' '.join([str(roll) for roll in dice_results])
		return 'You have rolled:\n' + ' '.join(result_string)
	except ValueError:
		return 'Hojicha is remembering something...'
	
	if mod_text[0]=='-':
		mod=mod*-1
	
	dice_results_mod = ['{dice_roll} ({orig})'.format(
	dice_roll=roll+mod,orig=roll) for roll in dice_results]

	#return "you asked for "+msg_args
	return 'You have rolled:\n' + ' '.join(dice_results_mod)




