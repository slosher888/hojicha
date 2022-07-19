#bot.py

import os
import discord
import datetime as dt
import subprocess
import hojicha_functions as hf
import requests
from dotenv import load_dotenv
import interactions as itr
#import interactions.ext.voice as iev

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
fortune_file=os.getenv('FORTUNE_DB_PATH')
guild_id=os.getenv('GID')
encoding='utf-8'
wakeup_time=dt.datetime.now()

client = itr.Client(token=TOKEN,
#	default_scope=guild_id,
	intents=itr.Intents.DEFAULT | itr.Intents.GUILD_MESSAGE_CONTENT)


#@client.event
#async def on_voice_state_update(vs: iev.VoiceState):
#        print(vs.self_mute)

@client.command(name="play_song",description="play a song", options=[])
async def play_song(ctx: itr.CommandContext):
    await client.connect_vc(channel_id=int(ctx.channel.id),guild_id=(ctx.guild_id),self_deaf=True,self_mute=False)
    await client.play(file="/home/csul/Downloads/chicken_fidler.mp3 ")




@client.command(
	name="cake",
	description="gives cake",
	options = [
		itr.Option(
			name="wants_extra",
			description="Want extra cake?",
			type=itr.OptionType.STRING,
			required=False,
		),
	],
)
async def cake(ctx: itr.CommandContext, wants_extra:str="False"):
	result="You have received "
	if wants_extra.lower()=="yes":
		result = result+"extra "
	result = result+"cake."
	await ctx.send(result)

@client.command(
	name="speak",
	description="Give words of wisdome (a la fortune)",
)
async def speak(ctx: itr.CommandContext):
	res = subprocess.check_output(['fortune',fortune_file])
	await ctx.send(res.decode(encoding))

@client.command(
	name="question",
	description="Ask a yes or no question",
	options = [
		itr.Option(
			name="text",
			description="Your inquiry",
			type=itr.OptionType.STRING,
			required=True,
		),
	],
)
async def question(ctx: itr.CommandContext, text:str):
	await ctx.send(hf.yes_no(text))


@client.command(
	name="uptime",
	description="How long has Hojicha been awake?",
)
async def uptime(ctx: itr.CommandContext):
	await ctx.send("I have been awake for "+ hf.hojicha_uptime(wakeup_time))

@client.command(
	name="draw_card",
	description="Draw a tarot card",
	options = [
		itr.Option(
			name="text",
			description="Your inquiry",
			type=itr.OptionType.STRING,
			required=False,
		),
	],
)
async def draw_card(ctx: itr.CommandContext, text:str=''):
	await ctx.send(hf.draw_a_tarot_card(text))


@client.command(
	name="t2b",
	description="Convert Text to binary",
	options = [
		itr.Option(
			name="text",
			description="Text to convert",
			type=itr.OptionType.STRING,
			required=True,
		),
	],
)
async def t2b(ctx: itr.CommandContext, text:str=''):
	#response_string=hf.text_to_binary(text)
	response_string="Converting the following to binary...\n**"+text+"**\n\n"
	binary_text=hf.text_to_binary(text)
	if(len(binary_text) > 20000):
		await ctx.send("Hojicha is watching that video where a guy opens up a $1300+ wheel of cheese.\n")
	else:
		await ctx.send(response_string+binary_text)

@client.command(
	name="b2t",
	description="Convert binary to text",
	options = [
		itr.Option(
			name="binary",
			description="Binary to convert",
			type=itr.OptionType.STRING,
			required=True,
		),
	],
)
async def b2t(ctx: itr.CommandContext, binary:str=''):
	#response_string=hf.text_to_binary(text)
	response_string="Converting the following to text...\n**"+binary+"**\n\n"
	#texted_binary=hf.text_from_bits(binary)
	texted_binary="aaaaaaah"
	if(len(texted_binary) > 20000):
		await ctx.send("Hojicha is watching that video where a guy opens up a $1300+ wheel of cheese.\n")
	else:
		#await ctx.send(response_string+texted_binary)
		await ctx.send(response_string+"Hojicha's asleep but wearing those glasses that make it seem like it's awake.")
@client.command(
	name="pick",
	description="Choose from a comma seperated list",
	options = [
		itr.Option(
			name="list",
			description="Your list of items",
			type=itr.OptionType.STRING,
			required=True,
		),
	],
)
async def pick(ctx: itr.CommandContext, list:str):
	await ctx.send(hf.pick_one(list))

@client.command(
	name="roll_dice",
	description="Roll N dice with M sides",
	options = [
		itr.Option(
			name="num_sides",
			description="Sides per die",
			type=itr.OptionType.INTEGER,
			required=False,
		),
		itr.Option(
			name="num_dice",
			description="How many dice to roll",
			type=itr.OptionType.INTEGER,
			required=False,
		),
		itr.Option(
			name="modifier",
			description="How much to add/subtract",
			type=itr.OptionType.INTEGER,
			required=False,
		),
	],
)
async def roll_dice(ctx: itr.CommandContext, num_sides:int=6, num_dice:int=1, modifier:int=0):
	await ctx.send(hf.roll_dice(num_dice,num_sides,modifier))

@client.command(
	name="c2f",
	description="Convert Celsus to Fahrenheit",
	options = [
		itr.Option(
			name="celsius",
			description="Celsius temp",
			type=itr.OptionType.NUMBER,
			required=True,
		),
	],
)
async def c_to_f(ctx: itr.CommandContext, celsius:float):
	fahrenheit=hf.c_to_f(celsius)
	await ctx.send(f"{celsius} C is {fahrenheit:.2f} F\n")

@client.command(
	name="f2c",
	description="Convert Fahrenheit to Celsius",
	options = [
		itr.Option(
			name="fahrenheit",
			description="Fahrenheit temp",
			type=itr.OptionType.NUMBER,
			required=True,
		),
	],
)
async def f_to_c(ctx: itr.CommandContext, fahrenheit:float):
	celsius=hf.f_to_c(fahrenheit)
	await ctx.send(f"{fahrenheit} F is {celsius:.2f} F\n")

client.start()

#@client.event
#async def on_ready():
#	print('We have logged in as {0.user}'.format(client))

#async def send_big_message(message,string):
#	filename=str(dt.datetime.now())+'.txt'
#	save_prefix='/tmp'
#	filepath=save_prefix+'/'+filename
#	response_file = open(filepath,'w')
#	max_len=80
#	chunks = [string[i:i+max_len] for i in range(0,len(string),max_len)]
#	for chunk in chunks:
#		response_file.write(chunk)
#		response_file.write('\n')
#	response_file.close()
#	response_file = open(filepath,'r')
#
#	discord_file=discord.File(response_file,filename)
#	await message.channel.send(file=discord_file)
#	response_file.close()
#
#@client.event
#async def on_message(message):
#	msg=message.content
#	if message.author == client.user:
#		return
#	if msg.startswith('!hojicha'):
#		msg_args=msg.split('!hojicha')
#		if msg_args[1]=='' or msg_args[1].upper()==' HI' or msg_args[1].upper()==' HELLO':
#			await message.channel.send('Hello!')
#		elif msg_args[1].upper()==' SPEAK':
#			res = subprocess.check_output(['fortune', fortune_file])
#			await message.channel.send(res.decode(encoding))
#		elif msg_args[1].upper().startswith(' Q'):
#			await message.channel.send(hf.yes_no(msg_args[1]))
#		elif msg_args[1].upper().startswith(' UPTIME'):
#			await message.channel.send("I have been awake for "+ hf.hojicha_uptime(wakeup_time))
#		elif msg_args[1].upper().startswith(' DRAW CARD'):
#			await message.channel.send(hf.draw_a_tarot_card(msg_args[1]))
#		elif msg_args[1].upper().startswith(' PICK'):
#			await message.channel.send(hf.pick_one(msg_args[1][6:]))
#		elif msg_args[1].upper().startswith(' ROLL'):
#			await message.channel.send(hf.roll_dice(msg_args[1].upper() ))
#		elif msg_args[1].upper().startswith(' T2B'):
#			if len(message.attachments)==1:
#				text_to_parse=requests.get(message.attachments[0].url).content.decode("utf-8")
#			else:
#				text_to_parse=msg_args[1][5:]
#
#			response_string=hf.text_to_binary(text_to_parse)
#			if len(response_string) > 2000:
#				await send_big_message(message,response_string)
#			else:
#				await message.channel.send(response_string)
#		elif msg_args[1].upper().startswith(' B2T'):
#			if len(message.attachments)==1:
#				text_to_parse=requests.get(message.attachments[0].url).content.decode("utf-8")
#			else:
#				text_to_parse=msg_args[1][5:]
#
#			response_string=hf.binary_to_text(text_to_parse)
#			if len(response_string) > 2000:
#				await send_big_message(message,response_string)
#			else:
#				await message.channel.send(response_string)
#		elif msg_args[1].upper().startswith(' HELP'):
#			await message.channel.send(hf.help_text())
#		else:
#			await message.channel.send('Hojicha slowly looks in your direction')
