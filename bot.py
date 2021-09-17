#bot.py

import os
import discord
import subprocess

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
encoding='utf-8'
fortune_file="/Users/csul/github/fortunes/fortunes"


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
		else:
			await message.channel.send('Hojicha slowly looks in your direction')
		
		


client.run(TOKEN)
