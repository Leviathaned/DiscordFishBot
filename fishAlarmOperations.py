import traceback

import pandas
from datetime import datetime, timezone, timedelta

import pandas as pd
import pytz

def getTimezoneData(jsonFile):
    try:
        df = pandas.read_json(jsonFile, dtype={"serverID": "int64"})
        if df.empty:
            df = pandas.DataFrame(columns = ["serverID", "timezone"])

    except KeyError:
        df = pandas.DataFrame(columns = ["serverID", "timezone"])
        print("There was a formatting issue with the entered .json file! Returning an empty formatted table...")

    return df

def saveTimezoneData(jsonFile, df):
    df.to_json(jsonFile)

def getFishingFridayData(jsonFile):
    """

    :param jsonFile:
    :return:

    This will return a pandas df of the enabledServers.json file.
    If the file does not exist, it will create a new one consisting of an empty dataframe
    """
    try:
        df = pandas.read_json(jsonFile, dtype={"serverID": "int64", "channelID": "int64", "fridayStage": "int64", "winningUser": "int64", "winningVoteCount": "int64"})

        if df.empty:
            df = pandas.DataFrame(columns=["serverID", "enabled", "channelID", "fridayStage", "winningComment", "winningUser", "winningVoteCount"])

    except KeyError:
        print("The inserted json was not formatted correctly! Resetting...")
        df = pandas.DataFrame(columns=["serverID", "enabled", "channelID", "fridayStage", "winningComment", "winningUser", "winningVoteCount"])

    return df

def saveFishingFridayData(jsonFile, df):
    df.to_json(jsonFile)

def getServerRow(df, serverID):
    """

    :param df:
    :param serverID:
    :return:
    This function returns a dataframe containing the row that shares the serverID listed. If there is no serverID,
    this function will return False.
    """
    df = df.loc[df["serverID"] == serverID]
    if df.empty:
        return False
    return df

def getCurrentTimeUTC():
    return datetime.now(timezone.utc)

def getCurrentTime(df, serverID):
    """
    :param df
    :param int serverID:
    :return:

    Insert a server that has an entry in the serverTimezones table to receive the localized time.
    If the server does not have an set timezone, this function will return False.
    """
    UTCTime = getCurrentTimeUTC()

    try:
        selectedServer = df[df['serverID'] == serverID]
        timezoneAdjust = UTCTime.astimezone(pytz.timezone(selectedServer['timezone'][selectedServer.index[0]]))
    except KeyError:
        return False
    return timezoneAdjust

def storeTimeZone(df, serverID, timezoneName):
    """
    :param df:
    :param serverID:
    :param string timezoneName:
    :return: none


    This function will save a timezone to a server. When calling the function, include the name of the server, and the name of the timezone.
    You can get the name of the timezone from fishAlarmOperations.convertHourOffset.
    """
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, timezoneName]

        df.loc[selectedServer.index] = [serverID, timezoneName]

        return df

    except (ValueError, KeyError):
        data = {"serverID": [serverID],
                "timezone": [timezoneName]}
        df = pd.DataFrame(data)
        return df

def setFishingFridayEnabled(df, serverID, enabled, channelID):
    """
    :param df
    :param serverID:
    :param Boolean enabled:
    :param String channelID:

    Will set a server's fishing friday status to the enabled variable, and will set the included channel as the fishing channel.
    """
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, enabled, channelID, 0, "None", -1, -1]

        df.loc[selectedServer.index] = [serverID, enabled, channelID, 0, "None", -1, -1]
    except (ValueError, KeyError):
        traceback.print_exc()
        data = {'serverID': [serverID],
                'enabled': [enabled],
                'channelID': [channelID],
                "fridayStage": [0],
                "winnerComment": "None",
                "winningUser": -1,
                "winningVoteCount": -1}
        df = pd.DataFrame(data)

    return df

def getFishingFridayInfo(df, serverID):
    """
    :param df:
    :param serverID:
    :return: Boolean enabledStatus

    This function will take a serverName and return if the server has enabled or disabled fishing friday alarms.
    """

    serverRow = df.loc[df["serverID"] == serverID]
    print(serverRow)
    return serverRow["enabled"]

def convertHourOffset(hourOffset):
    """
    :param int hourOffset:
    :return: string timezone

    This function takes a string in the form of an hour offset, such as '+4' or '-3'.
    It then returns a string usable by pytz to convert a datetime.
    """
    df = pandas.read_json("timezones.json")
    return df["timezones"][hourOffset]

def isItFriday(df, serverID):
    """
    :param df:
    :param serverID:
    :return: boolean isFriday

    This function returns whether or not it is friday in the timezone of the included serverID
    """
    currentTime = getCurrentTime(df, serverID)
    if currentTime.weekday() == 4:
        return True
    return False

def getTimeUntilFriday(currentTime):
    """

    :param datetime currentTime:
    :return: duration

    This function takes a datetime, and returns the duration until it is friday.
    It will return False if it is already friday.
    """
    currentDay = ((currentTime.weekday() + 2) % 7)
    if currentDay == 6:
        return False

    goalTime = currentTime + timedelta(hours = (6 - currentDay) * 24)
    goalTime = goalTime.replace(hour=0, minute=0, second=0, microsecond=0)
    return goalTime - currentTime

# functions to get json data into a df that check if the file exists

def checkAfterHour(df, serverID, targetHour):
    timestamp = getCurrentTime(df, serverID)

    if timestamp.hour > targetHour:
        return True
    return False

def incrementStage(df, serverID):
    """

    :param df:
    :param serverID:
    :return:
    """
    selectedServer = df[df["serverID"] == serverID]
    currentStage = selectedServer["fridayStage"][selectedServer.index[0]]
    df.at[selectedServer.index[0], 'fridayStage'] = currentStage + 1
    return df

def resetStage(df, serverID):
    selectedServer = df[df["serverID"] == serverID]
    df.at[selectedServer.index[0], 'fridayStage'] = 0
    return df

def saveWinningComment(df, serverID, comment, userID, voteCount):
    if df.empty:
        return
    selectedServer = df[df["serverID"] == serverID]
    df.at[selectedServer.index[0], 'winningComment'] = comment
    df.at[selectedServer.index[0], 'winningUser'] = userID
    df.at[selectedServer.index[0], 'winningVoteCount'] = voteCount
    return df

def getWinningComment(df, serverID):
    if df.empty:
        return
    selectedServer = df[df["serverID"] == serverID]
    print(selectedServer)
    winningComment = [0, 0, 0]
    winningComment[0] = selectedServer["winningComment"].tolist()[0]
    winningComment[1] = selectedServer["winningUser"].tolist()[0]
    winningComment[2] = selectedServer["winningVoteCount"].tolist()[0]
    return winningComment

def getFridayEnabledList(df):
    """
    :return: list of server ID

    This function will return a dataframe of all server IDs and channel ID's from servers that have fishing friday activated
    """
    if df.empty:
        return []

    newDF = df[df['enabled']]
    return newDF
