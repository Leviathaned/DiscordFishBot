import os

import traceback

import discord
from discord import option
from discord.ext import tasks

from dotenv import load_dotenv

import fishAlarmOperations
import fishFactOperations
import fishingFridayOperations

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

client = discord.Bot(command_prefix="+", intents=intents)

guild_ids = [844663929086935070, 721943963346665492, 412423098185416706]


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game('Use +help'))

@client.slash_command(name="hello", guild_ids=guild_ids, description="Say hello!")
async def hello(ctx):
    await ctx.respond("Hello!")

@client.slash_command(name="get_fish_fact", guild_ids=guild_ids, description="Get a random fish fact!")
@option("index",
        description = "Use this to find a specific fish fact!",
        required = False,
        default = '')
async def getFishFact(ctx, index: str):
    if index == '':
        await ctx.respond(fishFactOperations.grabFishFact(str(ctx.guild.id)))
        return
    try:
        await ctx.respond(fishFactOperations.grabSpecificFishFact(str(ctx.guild.id), int(index)))
    except:
        traceback.print_exc()
        await ctx.respond(
            f'That number is either too high, or not a number at all! For reference, I currently have {fishFactOperations.getFishFactCount(str(ctx.guild.id))} fish facts!')

@client.slash_command(name = "add_fish_fact", guild_ids=guild_ids, description = "Add a new fish fact!")
@option("fish_fact",
        description= "The new fish fact!",
        required = True)
async def addFishFact(ctx, fish_fact: str):
    try:
        fishFactOperations.addFishFact(str(ctx.guild.id), fish_fact)
        await ctx.respond(
            f"Fish fact '{fishFactOperations.getFishFactCount(str(ctx.guild.id))}) {fish_fact}' successfully added!")
    except:
        traceback.print_exc()
        await ctx.respond(
            "There was an issue adding the fish fact. Did you properly space the fact out, and keep it right after the command?")

@client.slash_command(name = "remove_fish_fact", guild_ids=guild_ids, description = "Remove a currently existing fish fact by index.")
@option("index",
        description="The fish fact to be deleted",
        required= True)
async def remove_fish_fact(ctx, index: str):
    await ctx.respond(
                f"Are you sure you want to remove the fish fact {fishFactOperations.grabSpecificFishFact(str(ctx.guild.id), int(index))} permanently? Please type 'Yes' to confirm, and anything else to cancel.")
    channel = ctx.channel

    def check(m):
        return m.channel == channel and m.author == ctx.author

    msg = await client.wait_for("message", check=check)
    if msg.content == "Yes":
        fishFactOperations.removeFishFact(str(ctx.guild.id), int(index))
        await ctx.respond("Ok, the fish fact has been deleted.")
    else:
        await ctx.respond("Ok, the delete command has been canceled.")

@client.slash_command(name="get_time", guild_ids=guild_ids, description="Get the current time!")
async def get_time(ctx):
    if not fishAlarmOperations.getCurrentTime(str(ctx.guild.id)):
        await ctx.respond("You have not set the server timezone!")
    else:
        await ctx.respond("The current time is " +
                          fishAlarmOperations.getCurrentTime(str(ctx.guild.id)).strftime("%m/%d/%y, %I:%M:%S %p") + " .")

@client.slash_command(name = "get_utc", guild_ids=guild_ids, description="Get the current UTC time!")
async def get_utc(ctx):
    await ctx.respond("The current UTC time is " +
                      fishAlarmOperations.getCurrentTimeUTC().strftime("%m/%d/%y, %I:%M:%S %p") + " .")

@client.slash_command(name = "set_timezone", guild_ids=guild_ids, description="Set the server time zone!")
async def set_timezone(ctx):
    await ctx.respond("The current UTC time is " +
                      fishAlarmOperations.getCurrentTimeUTC().strftime("%m/%d/%y, %I:%M:%S %p") + "." +
                      "Please input your time difference from UTC (for example, if you are 4 hours behind this time, input '-4', or '+4' if you are 4 hours ahead.)")
    channel = ctx.channel

    def check(m):
        return m.channel == channel and m.author == ctx.author

    msg = await client.wait_for("message", check=check)
    # A secondary check to ensure it is a integer
    try:
        timezoneName = fishAlarmOperations.convertHourOffset(int(msg.content))
        fishAlarmOperations.storeTimeZone(str(ctx.guild.id), timezoneName)
        await ctx.channel.send("Timezone set! The current time is " +
                               fishAlarmOperations.getCurrentTime(str(ctx.guild.id)).strftime("%m/%d/%y, %I:%M:%S %p"))
    except ValueError:
        await ctx.respond(
            "The input " + msg.content + " is not a valid response. Please make sure you use a positive or negative integer, and that it falls within the range of -12 to +11.")

@client.slash_command(name = "friday_status", guild_ids=guild_ids, description = "Set the server to be in fishing friday mode!")
@option(name="enable",
        description= "Set to True if you want fishing friday, set to False to disable fishing friday.",
        required = True)
async def friday_status(ctx, enable: bool):
    fishAlarmOperations.setFishingFridayEnabled(ctx.guild.id, enable)
    if enable:
        ctx.respond("Fishing friday has been enabled!")
        return
    ctx.respond("Fishing friday has been disabled!")

@client.slash_command(name="time_until_friday", guild_ids=guild_ids, description= "How much time until friday?")
async def time_until_friday(ctx):
    currentTime = fishAlarmOperations.getCurrentTime(str(ctx.guild.id))
    if not currentTime:
        await ctx.respond("You have not set your timezone!")
        return

    duration = fishAlarmOperations.getTimeUntilFriday(currentTime)
    if duration:
        await ctx.respond("It is already FISHING FRIDAY!!!")
        return

    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) - (hours * 60)
    seconds = duration.seconds - (minutes * 60) - (hours * 3600)
    await ctx.respond("Fishing friday is imminent...\nIt will be here in "
                               + str(duration.days) + " days, "
                               + str(hours) + " hours, "
                               + str(minutes) + " minutes, and "
                               + str(seconds) + " seconds. Be ready, brave fishers.")

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

+fridayStatus: Allows you to enable/disable this server to celebrate fishing friday!
+timeUntilFriday: How long until fishing friday?
""")
    # code pertaining to fish facts

    if userMessage[0] == '+getFishFact':
        if len(userMessage) == 1:
            await message.channel.send(fishFactOperations.grabFishFact(str(message.guild.id)))
        else:
            try:
                await message.channel.send(
                    fishFactOperations.grabSpecificFishFact(str(message.guild.id), int(userMessage[1])))
            except:
                traceback.print_exc()
                await message.channel.send(
                    f'That number is either too high, or not a number at all! For reference, I currently have {fishFactOperations.getFishFactCount(str(message.guild.id))} fish facts!')

    if userMessage[0] == '+addFishFact':
        try:
            fishFactOperations.addFishFact(str(message.guild.id), userMessage[1])
            await message.channel.send(
                f"Fish fact '{fishFactOperations.getFishFactCount(str(message.guild.id))}) {userMessage[1]}' successfully added!")
        except:
            await message.channel.send(
                "There was an issue adding the fish fact. Did you properly space the fact out, and keep it right after the command?")

    if userMessage[0] == '+removeFishFact':
        await message.channel.send(
            f"Are you sure you want to remove the fish fact {fishFactOperations.grabSpecificFishFact(str(message.guild.id), int(userMessage[1]))} permanently? Please type 'Yes' to confirm, and anything else to cancel.")
        channel = message.channel

        def check(m):
            return m.channel == channel and m.author == message.author

        msg = await client.wait_for("message", check=check)
        if msg.content == "Yes":
            fishFactOperations.removeFishFact(str(message.guild.id), int(userMessage[1]))
            await message.channel.send("Ok, the fish fact has been deleted.")
        else:
            await message.channel.send("Ok, the delete command has been canceled.")

    if userMessage[0] == "+getTime":
        if not fishAlarmOperations.getCurrentTime(str(message.guild.id)):
            await message.channel.send("You have not set the server timezone!")
        else:
            await message.channel.send("The current time is " +
                                       fishAlarmOperations.getCurrentTime(str(message.guild.id)).strftime(
                                           "%m/%d/%y, %I:%M:%S %p") + " .")

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
        # A secondary check to ensure it is a integer
        try:
            timezoneName = fishAlarmOperations.convertHourOffset(int(msg.content))
            fishAlarmOperations.storeTimeZone(str(message.guild.id), timezoneName)
            await message.channel.send("Timezone set! The current time is " +
                                       fishAlarmOperations.getCurrentTime(str(message.guild.id)).strftime(
                                           "%m/%d/%y, %I:%M:%S %p"))
        except ValueError:
            await message.channel.send(
                "The input " + msg.content + " is not a valid response. Please make sure you use a positive or negative integer, and that it falls within the range of -12 to +11.")

    if userMessage[0] == "+fridayStatus":
        enabledStatus = ["disabled", "enable", "enabled"]

        if fishAlarmOperations.getFishingFridayInfo(str(message.guild.id)):
            enabledStatus = ["enabled", "disable", "disabled"]

        await message.channel.send("Fishing friday is " + enabledStatus[0] + " for this server. "
                                   + "Would you like to " + enabledStatus[1] + " it? " +
                                   "If so, type in 'Yes'. To cancel, type in anything else.")
        channel = message.channel

        def check(m):
            return m.channel == channel and m.author == message.author

        msg = await client.wait_for("message", check = check)
        if msg.content == "Yes":
            await message.channel.send("Fishing friday is now " + enabledStatus[2] + "!")
            fishAlarmOperations.switchFishingFridayEnabled(str(message.guild.id))
        else:
            await message.channel.send("Alright, the command has been canceled.")

    if userMessage[0] == "+timeUntilFriday":
        currentTime = fishAlarmOperations.getCurrentTime(str(message.guild.id))
        if not currentTime:
            await message.channel.send("You have not set your timezone!")
            return

        duration = fishAlarmOperations.getTimeUntilFriday(currentTime)
        if duration:
            await message.channel.send("It is already FISHING FRIDAY!!!")
            return

        hours = duration.seconds // 3600
        minutes = (duration.seconds // 60) - (hours * 60)
        seconds = duration.seconds - (minutes * 60) - (hours * 3600)
        await message.channel.send("Fishing friday is imminent...\nIt will be here in "
                                   + str(duration.days) + " days, "
                                   + str(hours) + " hours, "
                                   + str(minutes) + " minutes, and "
                                   + str(seconds) + " seconds. Be ready, brave fishers.")

    # All of the fun activities to do on friday!
    if userMessage[0] == "+fishingFridayHelp":
        await message.channel.send("Welcome to fishing friday! Here are all of the available commands." +
                                   "These commands are ONLY available on friday!\n" +
                                   "'+fish': Go and fish! See what you catch!\n" +
                                   "'+comment': Comment what you caught! Try to come up with the best comment!")

    if userMessage[0] == "+fish":
        if not fishAlarmOperations.isItFriday(str(message.guild.id)):
            await message.channel.send("It is not friday yet!")
            return
        await message.channel.send("Function not fully implemented yet!")
        return

@tasks.loop(seconds = 10)
async def checkTime():
    guild = client.get_guild


client.run(TOKEN)
