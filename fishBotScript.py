import asyncio
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

debugServers = [844663929086935070, 1088123578966360114]

sentMessage = [0]
messagesList = []

factsFile = "fishFacts.json"
commentsFile = "fridayComments.json"
serverStatusFile = "enabledServers.json"
serverTimezoneFile = "serverTimezones.json"

def clearComments():
    fishingFridayOperations.clearFridayComments()
    messagesList.clear()

async def displayPreviousWinner(channel, serverList, serverIndex):
    await channel.send(fishingFridayOperations.grabFishingFridayMessage())

    df = fishAlarmOperations.getFishingFridayData(serverStatusFile)

    previousWinnerComment = fishAlarmOperations.getWinningComment(df, serverList[serverIndex])
    if not previousWinnerComment[0] == "None":
        await channel.send("The winner of the weekly comment competition last week was " + previousWinnerComment[
            1].name + "with the WONDERFUL comment: " + previousWinnerComment[0] + " boasting a POWERFUL " +
                           previousWinnerComment[
                               2] + "!\nWill anyone be able to beat them? Make sure to submit your comments by 6pm with /comment!")

    fishAlarmOperations.incrementStage(df, serverList[serverIndex])
    fishAlarmOperations.saveFishingFridayData(serverStatusFile, df)

async def displayComments(channel, serverList, serverIndex):
    await channel.send("Comment submission has ended! Here are the submitted comments:")
    fridayComments = fishingFridayOperations.readFridayCommentsData(commentsFile)
    fridayComments = fridayComments[fridayComments["serverID"] == serverList[serverIndex]]

    commentsList = fridayComments["comment"].tolist()
    userList = fridayComments["user"].tolist()

    serverMessagesList = []
    for i in range(0, len(commentsList)):
        user = client.get_user(userList[i])
        rankedMessage = await channel.send(commentsList[i] + " - " + user.name)
        serverMessagesList.append(rankedMessage.id)
        await rankedMessage.add_reaction("🔥")

    messagesList.append(serverMessagesList)

    await channel.send(
        "Place an fire emoji on your favorite comments! The comment with the most votes will win, and their comment will be kept for the next week!")
    df = fishAlarmOperations.getFishingFridayData(serverStatusFile)
    fishAlarmOperations.incrementStage(df, serverList[serverIndex])
    fishAlarmOperations.saveFishingFridayData(serverStatusFile, df)

async def displayWinningComment(channel, serverList, serverIndex):
    await channel.send("As fishing friday comes to a close, it is time to announce the winning comment!")

    print("These are all available comments listed in general")
    print(messagesList)
    print("Server Index: " + str(serverIndex))

    serverMessagesList = messagesList[serverIndex]
    winningMessage = ["None", "None", 0]

    fridayComments = fishingFridayOperations.readFridayCommentsData(commentsFile)
    fridayComments = fridayComments[fridayComments["serverID"] == serverList[serverIndex]]
    userList = fridayComments["user"].tolist()

    print("The available server Messages List are:")
    print(serverMessagesList)

    for i in range(0, len(serverMessagesList)):
        msg = await channel.fetch_message(serverMessagesList[i])
        fireReactions = discord.utils.get(msg.reactions, emoji="🔥").count
        if fireReactions > winningMessage[2]:
            print("Winning message found!")
            winningMessage = [msg.content, client.get_user(userList[i]), fireReactions]

    df = fishAlarmOperations.getFishingFridayData(serverStatusFile)
    await channel.send("Congratulations to " + str(winningMessage[1].name) + " for winning the comment competition!")
    await channel.send("\"" + (winningMessage[0]) + "\"")
    df = fishAlarmOperations.saveWinningComment(df, serverList[serverIndex], winningMessage[0], winningMessage[1].id,
                                                winningMessage[2])

    df = fishAlarmOperations.incrementStage(df, serverList[serverIndex])
    clearComments()
    fishAlarmOperations.saveFishingFridayData(serverStatusFile, df)

@tasks.loop(seconds = 10.0)
async def checkTime():
    baseDF = fishAlarmOperations.getFishingFridayData(serverStatusFile)
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)

    newDF = fishAlarmOperations.getFridayEnabledList(baseDF)
    serverList = newDF["serverID"].tolist()
    channelList = newDF["channelID"].tolist()
    enabledList = newDF["enabled"].tolist()
    fridayStageList = newDF["fridayStage"].tolist()

    for serverIndex in range(0, len(channelList)):
        currentStage = fridayStageList[serverIndex]
        if currentStage != 0 and not fishAlarmOperations.isItFriday(timezoneDF, serverList[serverIndex]):
            fishAlarmOperations.resetStage(baseDF, serverList[serverIndex])
            fishingFridayOperations.clearFridayComments()
            fishAlarmOperations.saveFishingFridayData(serverStatusFile, baseDF)
            return

        channel = client.get_channel(channelList[serverIndex])
        if enabledList[serverIndex] and fishAlarmOperations.isItFriday(timezoneDF, serverList[serverIndex]):

            if currentStage == 0 and fishAlarmOperations.checkAfterHour(timezoneDF, serverList[serverIndex], 12):
                await displayPreviousWinner(channel, serverList, serverIndex)
                fishAlarmOperations.incrementStage(baseDF, serverList[serverIndex])

            if currentStage == 1 and fishAlarmOperations.checkAfterHour(timezoneDF, serverList[serverIndex], 16):
                await channel.send("Make sure you've submitted your comments! Fishing Friday voting will happen in 2 hours!")
                fishAlarmOperations.incrementStage(baseDF, serverList[serverIndex])

            if currentStage == 2 and fishAlarmOperations.checkAfterHour(timezoneDF, serverList[serverIndex], 18):
                await displayComments(channel, serverList, serverIndex)

            # TODO: find a way to handle tie breakers here

            if currentStage == 3 and fishAlarmOperations.checkAfterHour(timezoneDF, serverList[serverIndex], 20):
                await displayWinningComment(channel, serverList, serverIndex)

        # reset code
    fishAlarmOperations.saveFishingFridayData(serverStatusFile, baseDF)

@client.event
async def on_ready():
    if not checkTime.is_running():
        checkTime.start()

    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game('IT IS FISHING FRIDAY!'))

@client.slash_command(name="hello", description="Say hello!")
async def hello(ctx):
    await ctx.respond("Hello!")

@client.slash_command(name="get_fish_fact", description="Get a random fish fact!")
@option("index",
        description = "Use this to find a specific fish fact!",
        required = False,
        default = '')
async def getFishFact(ctx, index: str):
    fishFactDf = fishFactOperations.readFishFactData(factsFile)
    if index == '':
        await ctx.respond(fishFactOperations.grabFishFact(fishFactDf, str(ctx.guild.id)))
        return
    try:
        await ctx.respond(fishFactOperations.grabSpecificFishFact(fishFactDf, str(ctx.guild.id), int(index)))
    except IndexError:
        traceback.print_exc()
        await ctx.respond(
            f'That number is either too high, or not a number at all! For reference, I currently have {fishFactOperations.getFishFactCount(fishFactDf, str(ctx.guild.id))} fish facts!')

@client.slash_command(name = "add_fish_fact", description = "Add a new fish fact!")
@option("fish_fact",
        description= "The new fish fact!",
        required = True)
async def addFishFact(ctx, fish_fact: str):
    try:
        fishFactDf = fishFactOperations.readFishFactData(factsFile)
        fishFactOperations.addFishFact(fishFactDf, str(ctx.guild.id), fish_fact)
        await ctx.respond(
            f"Fish fact '{fishFactOperations.getFishFactCount(fishFactDf, str(ctx.guild.id))}) {fish_fact}' successfully added!")
        fishFactOperations.saveFishFactData(fishFactDf, factsFile)
    except IndexError:
        traceback.print_exc()
        await ctx.respond(
            "There was an issue adding the fish fact. Did you properly space the fact out, and keep it right after the command?")

@client.slash_command(name = "remove_fish_fact", description = "Remove a currently existing fish fact by index.")
@option("index",
        description="The fish fact to be deleted",
        required= True)
async def remove_fish_fact(ctx, index: str):
    fishFactDf = fishFactOperations.readFishFactData(factsFile)
    await ctx.respond(
                f"Are you sure you want to remove the fish fact {fishFactOperations.grabSpecificFishFact(fishFactDf, str(ctx.guild.id), int(index))} permanently? Please type 'Yes' to confirm, and anything else to cancel.")
    channel = ctx.channel

    def check(m):
        return m.channel == channel and m.author == ctx.author

    msg = await client.wait_for("message", check=check)
    if msg.content == "Yes":
        fishFactOperations.removeFishFact(fishFactDf, str(ctx.guild.id), int(index))
        await ctx.respond("Ok, the fish fact has been deleted.")
    else:
        await ctx.respond("Ok, the delete command has been canceled.")

    fishFactOperations.saveFishFactData(fishFactDf, factsFile)

@client.slash_command(name="get_time", description="Get the current time!")
async def get_time(ctx):
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)

    if not fishAlarmOperations.getCurrentTime(timezoneDF, ctx.guild.id):
        await ctx.respond("You have not set the server timezone!")
    else:
        await ctx.respond("The current time is " +
                          fishAlarmOperations.getCurrentTime(timezoneDF, ctx.guild.id).strftime("%m/%d/%y, %I:%M:%S %p") + " .")

@client.slash_command(name = "get_utc", description="Get the current UTC time!")
async def get_utc(ctx):
    await ctx.respond("The current UTC time is " +
                      fishAlarmOperations.getCurrentTimeUTC().strftime("%m/%d/%y, %I:%M:%S %p") + " .")

@client.slash_command(name = "set_timezone", description="Set the server time zone!")
async def set_timezone(ctx):
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)
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
        timezoneDF = fishAlarmOperations.storeTimeZone(timezoneDF, ctx.guild.id, timezoneName)
        await ctx.channel.send("Timezone set! The current time is " +
                               fishAlarmOperations.getCurrentTime(timezoneDF, ctx.guild.id).strftime("%m/%d/%y, %I:%M:%S %p"))
    except ValueError:
        await ctx.respond(
            "The input " + msg.content + " is not a valid response. Please make sure you use a positive or negative integer, and that it falls within the range of -12 to +11.")

@client.slash_command(name = "friday_status", description = "Enable fishing friday bot commands in the current channel.")
@option(name="enable",
        description= "Set to True if you want fishing friday, set to False to disable fishing friday.",
        required = True)
async def friday_status(ctx, enable: bool):
    statusDF = fishAlarmOperations.getFishingFridayData(serverStatusFile)

    fishAlarmOperations.setFishingFridayEnabled(statusDF, ctx.guild.id, enable, ctx.channel.id)

    if enable:
        await ctx.respond("Fishing friday has been enabled! The channel '#" + ctx.channel.name + "' will be the fishing channel from here on out!"
                          + "To change the fishing channel, re-run this command in the desired channel.")
        return
    await ctx.respond("Fishing friday has been disabled!")

@client.slash_command(name="time_until_friday", description= "How much time until friday?")
async def time_until_friday(ctx):
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)

    currentTime = fishAlarmOperations.getCurrentTime(timezoneDF, ctx.guild.id)
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

@client.slash_command(name="fish", description="Catch a fish to celebrate fishing friday!")
async def fish(ctx):
    caughtFish = fishingFridayOperations.fish()
    link = "https://en.wikipedia.org/wiki/" + caughtFish.replace(" ", "_")
    await ctx.respond("You caught a " + caughtFish + "!\n" + link)

@client.slash_command(name="comment", description="Comment what you caught on fishing friday!")
@option(name="user_comment",
        description= "What is your comment?",
        required = True)
async def comment(ctx, user_comment: str):
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)
    if not fishAlarmOperations.isItFriday(timezoneDF, ctx.guild.id):
        await ctx.respond("It is not fishing friday yet.\nBe patient, powerful fisher.")
        return

    df = fishingFridayOperations.readFridayCommentsData(commentsFile)

    exists = fishingFridayOperations.checkIfUserCommentExists(df, ctx.guild.id, ctx.author.id)
    if not isinstance(exists, str):
        fishingFridayOperations.addComment(df, ctx.guild.id, user_comment, ctx.author.id)
        await ctx.respond("Your comment '" + user_comment + "' has been successfully added!")
        fishingFridayOperations.saveFridayCommentsData(commentsFile, df)
        return

    msg = await ctx.send(
        "You already have the submitted comment '" + exists + "' for today! Would you like to replace it?")
    emojiCheck = "✅"
    emojiCross = "❌"
    await msg.add_reaction(emojiCheck)
    await msg.add_reaction(emojiCross)

    await ctx.respond("React with a check to change the message, and an X to keep your current one.")

    def check(userReaction, selectedUser):
        return selectedUser == ctx.author and (str(userReaction.emoji) == emojiCheck or str(userReaction.emoji) == emojiCross)

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=30.0, check=check)

        if reaction.emoji == "✅":
            fishingFridayOperations.addComment(df, ctx.guild.id, user_comment, ctx.author.id)
            await ctx.respond("Alright, your new comment is '" + user_comment + "'")
            fishingFridayOperations.saveFridayCommentsData(commentsFile, df)
            return
        else:
            await ctx.respond("Alright, the comment change has been canceled.")
            return
    except asyncio.TimeoutError or asyncio.CancelledError:
        await ctx.respond("You haven't responded, so I'll keep the comment the way it is!")
        return


@client.slash_command(name="view_comment", description="View your submitted comment!")
async def viewComment(ctx):

    df = fishingFridayOperations.readFridayCommentsData(commentsFile)
    timezoneDF = fishAlarmOperations.getTimezoneData(serverTimezoneFile)

    if not fishAlarmOperations.isItFriday(timezoneDF, ctx.guild.id):
        await ctx.respond("It is not fishing friday.\nBe patient, vigilant fisher...")
        return
    userComment = fishingFridayOperations.checkIfUserCommentExists(df, ctx.guild.id, ctx.author.id)
    if not isinstance(userComment, str):
        await ctx.respond("You do not have a comment currently submitted!")
        return
    await ctx.respond("Your wonderful comment is " + userComment + ".")

@client.slash_command(name="debug_comment", guild_ids= debugServers, description="Adding a comment under the current user.")
@option(name="user_comment",
        description= "What is your comment?",
        required = True)
async def debugComment(ctx, user_comment: str):
    df = fishingFridayOperations.readFridayCommentsData(commentsFile)

    exists = fishingFridayOperations.checkIfUserCommentExists(df, ctx.guild.id, ctx.author.id)
    if not isinstance(exists, str):
        fishingFridayOperations.addComment(df, ctx.guild.id, user_comment, ctx.author.id)
        await ctx.respond("Your comment '" + user_comment + "' has been successfully added!")
        return

    await ctx.respond("You already have the submitted comment '" + exists + "' for today! Would you like to replace it? Type Yes to replace, or anything else to cancel.")

    channel = ctx.channel

    def check(m):
        return m.channel == channel and m.author == ctx.author

    msg = await client.wait_for("message", check=check)
    if msg.content == "Yes":
        fishingFridayOperations.addComment(df, ctx.guild.id, user_comment, ctx.author.id)
        await ctx.respond("Alright, your new comment is '" + user_comment + "'")
        return
    await ctx.respond("Alright, the comment change has been canceled.")

    fishingFridayOperations.saveFridayCommentsData(commentsFile, df)

@client.slash_command(name="see_comment_debug", guild_ids= debugServers, description="View your currently submitted comment.")
async def seeCommentDebug(ctx):
    df = fishingFridayOperations.readFridayCommentsData(commentsFile)

    userComment = fishingFridayOperations.checkIfUserCommentExists(df, ctx.guild.id, ctx.author.id)
    if not isinstance(userComment, str):
        await ctx.respond("You do not have a comment currently submitted!")
        return
    await ctx.respond("Your wonderful comment is " + userComment + ".")

@client.slash_command(name="place_reaction_message", guild_ids= debugServers, description="Set down a base reaction message.")
async def placeReactionMessage(ctx):
    await ctx.respond("Sending generic message...")
    reactionMessage = await ctx.channel.send("Here is a generic message!")
    await reactionMessage.add_reaction(emoji="🔥")
    sentMessage[0] = reactionMessage.id

@client.slash_command(name="check_message_reactions", guild_ids=debugServers, description="Check the reaction stats on the previously placed message")
async def checkMessageReactions(ctx):
    reactionMessage = await ctx.fetch_message(sentMessage[0])
    currentReactions = discord.utils.get(reactionMessage.reactions, emoji="🔥")
    await ctx.respond("The amount of fire emojis on the message is " + str(currentReactions.count))

@client.slash_command(name="check_previous_winner", guild_ids=debugServers, description="Check the previous winner of the comment!")
async def checkPreviousWinner(ctx):
    statusDF = fishAlarmOperations.getFishingFridayData(serverStatusFile)

    newDF = fishAlarmOperations.getFridayEnabledList(statusDF)
    serverList = newDF["serverID"].tolist()

    for serverIndex in range(0, len(serverList)):
        await displayPreviousWinner(ctx.channel, serverList, serverIndex)

@client.slash_command(name="check_all_comments", guild_ids=debugServers, description="Display all comments and vote on them!")
async def checkCurrentComments(ctx):
    statusDF = fishAlarmOperations.getFishingFridayData(serverStatusFile)

    newDF = fishAlarmOperations.getFridayEnabledList(statusDF)
    serverList = newDF["serverID"].tolist()

    for serverIndex in range(0, len(serverList)):
        await displayComments(ctx.channel, serverList, serverIndex)

@client.slash_command(name="check_winner_comment", guild_ids=debugServers, description="check which comment is the winner!")
async def checkWinnerComment(ctx):
    statusDF = fishAlarmOperations.getFishingFridayData(serverStatusFile)

    newDF = fishAlarmOperations.getFridayEnabledList(statusDF)
    serverList = newDF["serverID"].tolist()

    for serverIndex in range(0, len(serverList)):
        await displayWinningComment(ctx.channel, serverList, serverIndex)

@client.slash_command(name="clear_comment_cache", guild_ids=debugServers, description="clear all comments being saved and voted upon for this friday!")
async def clearCommentCache(ctx):
    clearComments()

client.run(TOKEN)
