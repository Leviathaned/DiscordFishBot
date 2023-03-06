import os

import traceback

import discord
from discord.ext import commands

from dotenv import load_dotenv

import fishAlarmOperations
import fishFactOperations

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = commands.Bot(command_prefix="+", intents=intents)

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
    else:
        return

    if userMessage[0] == '+hello':
        await message.channel.send("Hello World!")

    if userMessage[0] == '+help':
        await message.channel.send("""
Hello! I am the fishing bot! Here are the commands I currently support:
    
+hello: Hi!
+getFishFact <index>: Listen to one of my many fish facts! Use the index to choose a specific number.
+addFishFact <fish fact>: Add onto my collection of fish facts!
+removeFishFact <index>: Remove one of my fish facts by index!
+help: Get info about my commands!
+setTimezone: set the timezone for the server.
+getTime: get the time based on the server.
+getUTC: get the current UTC time.
""")
    # code pertaining to fish facts

    if userMessage[0] == '+getFishFact':
        if len(userMessage) == 1:
            await message.channel.send(fishFactOperations.grabFishFact(message.guild.name))
        else:
            try:
                await message.channel.send(
                    fishFactOperations.grabSpecificFishFact(message.guild.name, int(userMessage[1])))
            except:
                traceback.print_exc()
                await message.channel.send(
                    f'That number is either too high, or not a number at all! For reference, I currently have {fishFactOperations.getFishFactCount(message.guild.name)} fish facts!')

    if userMessage[0] == '+addFishFact':
        try:
            fishFactOperations.addFishFact(message.guild.name, userMessage[1])
            await message.channel.send(
                f"Fish fact '{fishFactOperations.getFishFactCount(message.guild.name)}) {userMessage[1]}' successfully added!")
        except:
            await message.channel.send(
                "There was an issue adding the fish fact. Did you properly space the fact out, and keep it right after the command?")

    if userMessage[0] == '+removeFishFact':
        await message.channel.send(
            f"Are you sure you want to remove the fish fact {fishFactOperations.grabSpecificFishFact(message.guild.name, int(userMessage[1]))} permanently? Please type 'Yes' to confirm, and anything else to cancel.")
        channel = message.channel

        def check(m):
            return m.channel == channel and m.author == message.author

        msg = await client.wait_for("message", check=check)
        if msg.content == "Yes":
            fishFactOperations.removeFishFact(message.guild.name, int(userMessage[1]))
            await message.channel.send("Ok, the fish fact has been deleted.")
        else:
            await message.channel.send("Ok, the delete command has been canceled.")

    if userMessage[0] == "+getTime":
        if not fishAlarmOperations.getCurrentTime(message.guild.name):
            await message.channel.send("You have not set the server timezone!")
        else:
            await message.channel.send("The current time is " +
                                       fishAlarmOperations.getCurrentTime(message.guild.name).strftime("%m/%d/%y, %I:%M:%S %p") + " .")

    if userMessage[0] == "+getUTC":
        await message.channel.send("The current UTC time is " +
                                   fishAlarmOperations.getCurrentTimeUTC().strftime("%m/%d/%y, %I:%M:%S %p") + " .")

    # Code pertaining to fishingFriday Alarm
    if userMessage[0] == "+setTimezone":
        await message.channel.send("The current UTC time is " +
                                   fishAlarmOperations.getCurrentTimeUTC().strftime("%m/%d/%y, %I:%M:%S %p") + "." +
                                   "Please input your time difference from UTC (for example, if you are 4 hours behind this time, input '-4', or '+4' if you are 4 hours ahead.)")
        channel = message.channel

        def check(m):
            return m.channel == channel and m.author == message.author

        msg = await client.wait_for("message", check=check)
        #A secondary check to ensure it is a integer
        try:
            timezoneName = fishAlarmOperations.convertHourOffset(int(msg.content))
            fishAlarmOperations.storeTimeZone(message.guild.name, timezoneName)
            await message.channel.send("Timezone set! The current time is " +
                                       fishAlarmOperations.getCurrentTime(message.guild.name).strftime("%m/%d/%y, %I:%M:%S %p"))
        except ValueError:
            await message.channel.send("The input " + msg.content + " is not a valid response. Please make sure you use a positive or negative integer, and that it falls within the range of -12 to +11.")


client.run(TOKEN)
