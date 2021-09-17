#bot.py

import os
import discord
import subprocess
import random

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
encoding='utf-8'
fortune_file="/Users/csul/github/fortunes/fortunes"


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
			action='shakes it\'s head'
		response='Hojicha {act}{mod}.'
		return response.format(act=action,mod=modifier)
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
		else:
			await message.channel.send('Hojicha slowly looks in your direction')




client.run(TOKEN)
