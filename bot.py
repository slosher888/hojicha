#bot.py

import os
import discord
import subprocess
import random
import humanize
import datetime as dt
import requests

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
fortune_file=os.getenv('FORTUNE_DB_PATH')
encoding='utf-8'
wakeup_time=dt.datetime.now()

def draw_a_tarot_card(msg_args):
	response=requests.get('https://rws-cards-api.herokuapp.com/api/v1/cards/random?n=1').json()
	card=response['cards'][0]
	orientation=' '+random.choice(['right side up.','upside down.'])

	result='You have drawn '+ card['name']+orientation+'\n'
	result +='\nMeaning up:\n'
	result += card['meaning_up']
	result +='\n\nMeaning down:\n'
	result += card['meaning_rev']
	return result



def yes_no():
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
		response='Hojicha {act}{mod}.'
		return response.format(act=action,mod=modifier)
def hojicha_uptime():
	return humanize.naturaltime(dt.datetime.now()-wakeup_time)[:-4]+'.'

client = discord.Client()
#event_df= {
	#'Server':[client.server_name],
	#'Event Name':['wake_up_hojicha'],
	#'Event Time':[dt.datetime.now()],
#}

#def time_since_event(df):
#		last_time=df[
#		(df['Server'=='Silent Running']) &
#		(df['Event Name'=='uv catastrophe']) &
#		].iloc[0]['Event time']
#		humanize.naturaltime(dt.datetime.now()-last_time)


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	msg=message.content
	if message.author == client.user:
		return
	if msg.startswith('!hojicha'):
		msg_args=msg.split('!hojicha')
		if msg_args[1]=='' or msg_args[1].upper()==' HI' or msg_args[1].upper()==' HELLO':
			await message.channel.send('Hello!')
		elif msg_args[1].upper()==' SPEAK':
			res = subprocess.check_output(['fortune', fortune_file])
			await message.channel.send(res.decode(encoding))
		elif msg_args[1].upper().startswith(' Q'):
			await message.channel.send(yes_no())
		elif msg_args[1].upper().startswith(' UPTIME'):
			await message.channel.send("I have been awake for "+ hojicha_uptime())
		elif msg_args[1].upper().startswith(' DRAW CARD'):
			await message.channel.send(draw_a_tarot_card(msg_args[1]))
		else:
			await message.channel.send('Hojicha slowly looks in your direction')




client.run(TOKEN)
