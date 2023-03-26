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

guild_ids = []

@tasks.loop(seconds = 10.0)
async def checkTime():

    newDF = fishAlarmOperations.getFridayEnabledList()
    serverList = newDF["serverID"].tolist()
    channelList = newDF["channelID"].tolist()
    enabledList = newDF["enabled"].tolist()
    fridayStageList = newDF["fridayStage"].tolist()

    for serverIndex in range(0, len(channelList)):
        currentStage = fridayStageList[serverIndex]
        channel = client.get_channel(channelList[serverIndex])
        if enabledList[serverIndex] and fishAlarmOperations.isItFriday(serverList[serverIndex]):
            if currentStage == 0 and fishAlarmOperations.checkAfterHour(serverList[serverIndex], 12):
                await channel.send(fishingFridayOperations.grabFishingFridayMessage())
                fishAlarmOperations.incrementStage(serverList[serverIndex])

            if currentStage == 1 and fishAlarmOperations.checkAfterHour(serverList[serverIndex], 16):
                await channel.send("Make sure you've submitted your comments (impossible)! Fishing Friday voting will happen in 2 hours!")
                fishAlarmOperations.incrementStage(serverList[serverIndex])

            if currentStage == 2 and fishAlarmOperations.checkAfterHour(serverList[serverIndex], 18):
                await channel.send("Comment submission has ended! Here are the submitted comments:")
                # list off comments and hold onto ID's here
                await channel.send("Place an emote on your favorite comment! The comment with the most votes will win, and their comment will be kept for the next week!")
                fishAlarmOperations.incrementStage(serverList[serverIndex])

            # TODO: find a way to handle tie breakers here

            if currentStage == 3 and fishAlarmOperations.checkAfterHour(serverList[serverIndex], 20):
                await channel.send("As fishing friday comes to a close, it is time to announce the winning comment!(impossible)")
                await channel.send("Congratulations to Levi! He is so cool and awesome :)")

        #reset code
        if currentStage != 0 and not fishAlarmOperations.isItFriday(serverList[serverIndex]):
            fishAlarmOperations.resetStage(serverList[serverIndex])


@client.event
async def on_ready():
    checkTime.start()
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
    if not fishAlarmOperations.getCurrentTime(ctx.guild.id):
        await ctx.respond("You have not set the server timezone!")
    else:
        await ctx.respond("The current time is " +
                          fishAlarmOperations.getCurrentTime(ctx.guild.id).strftime("%m/%d/%y, %I:%M:%S %p") + " .")

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
        fishAlarmOperations.storeTimeZone(ctx.guild.id, timezoneName)
        await ctx.channel.send("Timezone set! The current time is " +
                               fishAlarmOperations.getCurrentTime(ctx.guild.id).strftime("%m/%d/%y, %I:%M:%S %p"))
    except ValueError:
        await ctx.respond(
            "The input " + msg.content + " is not a valid response. Please make sure you use a positive or negative integer, and that it falls within the range of -12 to +11.")

@client.slash_command(name = "friday_status", guild_ids=guild_ids, description = "Enable fishing friday bot commands in the current channel.")
@option(name="enable",
        description= "Set to True if you want fishing friday, set to False to disable fishing friday.",
        required = True)
async def friday_status(ctx, enable: bool):

    fishAlarmOperations.setFishingFridayEnabled(ctx.guild.id, enable, ctx.channel.id)

    if enable:
        await ctx.respond("Fishing friday has been enabled! The channel '#" + ctx.channel.name + "' will be the fishing channel from here on out!"
                          + "To change the fishing channel, re-run this command in the desired channel."
                          + str(ctx.channel.id))
        return
    await ctx.respond("Fishing friday has been disabled!")

@client.slash_command(name="time_until_friday", guild_ids=guild_ids, description= "How much time until friday?")
async def time_until_friday(ctx):
    currentTime = fishAlarmOperations.getCurrentTime(ctx.guild.id)
    if not currentTime:
        await ctx.respond("You have not set your timezone!")
        return

    duration = fishAlarmOperations.getTimeUntilFriday(currentTime)
    if not duration:
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


client.run(TOKEN)
