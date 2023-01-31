import random
import os

import traceback
import csv

from discord.utils import get
import discord
from discord.ext import commands

from dotenv import load_dotenv

def grabCSVRows():
	with open('fishFacts.csv', 'r') as fd:
		reader = csv.reader(fd)
		return sum(1 for row in reader)
		fd.close()

def grabFishFact():
	fishFactList = []
	
	with open('fishFacts.csv', 'r') as fd:
		reader = csv.reader(fd)
		for row in reader:
			fishFactList.append(row[0])
	fd.close()
	
	randomFactIndex = random.randint(0, len(fishFactList) - 1)
	return str(randomFactIndex + 1) + ') ' + fishFactList[randomFactIndex]
	
def grabSpecificFishFact(i):
	fishFactList = []
	
	with open('fishFacts.csv', 'r') as fd:
		reader = csv.reader(fd)
		for row in reader:
			fishFactList.append(row[0])
	fd.close()
	return str(i + 1) + ') ' + fishFactList[i] 
	
def addFishFact(fishFact):
	row = [fishFact]
	with open('fishFacts.csv', 'a') as fd:
		writer = csv.writer(fd)
		writer.writerow(row)
		fd.close()
		
def removeFishFact(index):
	fishFactList = []
	
	with open('fishFacts.csv', 'r') as fd:
		reader = csv.reader(fd)
		for row in reader:
			fishFactList.append(row[0])
	fd.close()
	del fishFactList[index]
	
	with open('fishFacts.csv', 'w') as fd:
		writer = csv.writer(fd)
		for fact in fishFactList:
			writer.writerow([fact])
	fd.close()
	return

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = commands.Bot(command_prefix = "+", intents=intents)

@client.event
async def on_ready():
		print(f'{client.user} has connected to Discord!')
		await client.change_presence(activity=discord.Game('Use +help'))
		
@client.event
async def on_message(message):
	if message.author == client.user:
		return
		
	if message.content.startswith('+'):
		userMessage = message.content.split(" ", 1)
		
		if userMessage[0] == '+hello!':
			await message.channel.send("Hello World!")
		
		if userMessage[0] == '+help':
			await message.channel.send("""
			Hello! I am the fishing bot! Here are the commands I currently support:
			
		+hello: Hi!
		+getFishFact <index>: Listen to one of my many fish facts! Use the index to choose a specific number.
		+addFishFact <fish fact>: Add onto my collection of fish facts!
		+removeFishFact <index>: Remove one of my fish facts by index!
		+help: Get info about my commands!
		""")
			
		if userMessage[0] == '+getFishFact':
			if len(userMessage) == 1:
				await message.channel.send(grabFishFact())
			else:
				try:
					await message.channel.send(grabSpecificFishFact(int(userMessage[1]) - 1))
				except:
					traceback.print_exc()
					await message.channel.send(f'That number is either too high, or not a number at all! For reference, I currently have {grabCSVRows()} fish facts!')
			
			
			
		if userMessage[0] == '+addFishFact':
			try:
				addFishFact(userMessage[1])
				await message.channel.send(f"Fish fact '{grabCSVRows()}) {userMessage[1]}' successfully added!")
			except:
				await message.channel.send("There was an issue adding the fish fact. Did you properly space the fact out, and keep it right after the command?")
		
		
		if userMessage[0] == '+removeFishFact':
			await message.channel.send(f"Are you sure you want to remove the fish fact {grabSpecificFishFact(int(userMessage[1]) - 1)} permanently? Please type 'Yes' to confirm, and anything else to cancel.")
			channel = message.channel
			
			def check(m):
				return m.channel == channel and m.author == message.author
				
			msg = await client.wait_for("message", check=check)
			if msg.content == "Yes":
				removeFishFact(int(userMessage[1]) - 1)
				await message.channel.send("Ok, the fish fact has been deleted.")
			else:
				await message.channel.send("Ok, the delete command has been canceled.")
				
			
client.run(TOKEN)
