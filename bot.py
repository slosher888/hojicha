#bot.py

import os
import discord
import subprocess
import random
import humanize
import datetime as dt

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
fortune_file=os.getenv('FORTUNE_DB_PATH')
encoding='utf-8'
wakeup_time=dt.datetime.now()

def help_text():
	string=          'Hiii, I know the following commands:\n'
	string = string+ 'SPEAK  Give words of wisdom (a la fortune)\n'
	string = string+ 'PICK   Select from comma seperated list\n'
	string = string+ 'Q      Answer yes/no question\n'
	string = string+ 'HELP   Display this message, obvs\n'
	return string
	#string = string+ '\n'

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

def yes_no():
		conviction=random.randint(0,9)
		modifier=''
		action=''

		if conviction >= 0 and conviction <= 3:
			modifier=' a bit'
		if conviction > 3 and conviction <= 6:
			modifier=''
		if conviction > 6:
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
		elif msg_args[1].upper().startswith(' PICK'):
			await message.channel.send(pick_one(msg_args[1][6:]))
		elif msg_args[1].upper().startswith(' HELP'):
			await message.channel.send(help_text())
		else:
			await message.channel.send('Hojicha slowly looks in your direction')




client.run(TOKEN)
