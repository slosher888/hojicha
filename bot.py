#bot.py

import os
import discord
from discord.utils import get
import datetime as dt
import subprocess
import hojicha_functions as hf
import requests
from dotenv import load_dotenv
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
fortune_file=os.getenv('FORTUNE_DB_PATH')
encoding='utf-8'
wakeup_time=dt.datetime.now()

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

async def send_big_message(message,string):
	filename=str(dt.datetime.now())+'.txt'
	save_prefix='/tmp'
	filepath=save_prefix+'/'+filename
	response_file = open(filepath,'w')
	max_len=80
	chunks = [string[i:i+max_len] for i in range(0,len(string),max_len)]
	for chunk in chunks:
		response_file.write(chunk)
		response_file.write('\n')
	response_file.close()
	response_file = open(filepath,'r')

	discord_file=discord.File(response_file,filename)
	await message.channel.send(file=discord_file)
	response_file.close()

@client.event
async def on_message(message):
	msg=message.content
	if message.author == client.user:
		return
	if msg.startswith('!hojicha'):
		msg_args=msg.split('!hojicha')
		msg_arg_list=msg_args[1].split(' ')
		if msg_args[1]=='' or msg_args[1].upper()==' HI' or msg_args[1].upper()==' HELLO':
			await message.channel.send('Hello!')
		elif msg_args[1].upper()==' SPEAK':
			res = subprocess.check_output(['fortune', fortune_file])
			await message.channel.send(res.decode(encoding))
		elif msg_args[1].upper().startswith(' Q'):
			await message.channel.send(hf.yes_no(msg_args[1]))
		elif msg_args[1].upper().startswith(' UPTIME'):
			await message.channel.send("I have been awake for "+ hf.hojicha_uptime(wakeup_time))
		elif msg_args[1].upper().startswith(' DRAW CARD'):
			await message.channel.send(hf.draw_a_tarot_card(msg_args[1]))
		elif msg_args[1].upper().startswith(' PICK'):
			await message.channel.send(hf.pick_one(msg_args[1][6:]))
		elif msg_args[1].upper().startswith(' ROLL'):
			await message.channel.send(hf.roll_dice(msg_args[1].upper() ))
		elif msg_args[1].upper().startswith(' T2B'):
			if len(message.attachments)==1:
				text_to_parse=requests.get(message.attachments[0].url).content.decode("utf-8")
			else:
				text_to_parse=msg_args[1][5:]

			response_string=hf.text_to_binary(text_to_parse)
			if len(response_string) > 2000:
				await send_big_message(message,response_string)
			else:
				await message.channel.send(response_string)
		elif msg_args[1].upper().startswith(' B2T'):
			if len(message.attachments)==1:
				text_to_parse=requests.get(message.attachments[0].url).content.decode("utf-8")
			else:
				text_to_parse=msg_args[1][5:]

			response_string=hf.binary_to_text(text_to_parse)
			if len(response_string) > 2000:
				await send_big_message(message,response_string)
			else:
				await message.channel.send(response_string)
		# bonk
		elif msg_args[1].upper().startswith(' BONK'):
			try:
				bonk_id,bonk_duration=hf.bonk(msg_arg_list[2:])
				if duration >= 60*60: # one hour
					await message.channel.send('Hojichas is admiring the bonk hammer and didn\'t hear you.')
				else:
					user2bonk= message.mentions[0]
					uname=user2bonk.display_name
					role=get(message.guild.roles,name='BONKED')
					await user2bonk.add_roles(role)
					await message.channel.send('Hojicha bonks {user} for {duration}s'.format(user=uname,duration=bonk_duration))
					await asyncio.sleep(bonk_duration)
					await user2bonk.remove_roles(role)
					await message.channel.send('Hojicha unbonks {user}'.format(user=uname))


			except ValueError:
				await message.channel.send('Hojicha doesn\'t understand, try \'!hojicha help\' ?')

		# un bonk
		elif msg_args[1].upper().startswith(' UNBONK ME'):
			role=get(message.guild.roles, name='bonked')
			await message.author.remove_roles(role)
			if(message.author.nick=='None'):
				uname=message.author.nick
			else:
				uname=message.author.name
			await message.channel.send('Hojicha unbonks {user}'.format(user=uname))


		elif msg_args[1].upper().startswith(' HELP'):
			await message.channel.send(hf.help_text())
		else:
			await message.channel.send('Hojicha slowly looks in your direction')




client.run(TOKEN)
