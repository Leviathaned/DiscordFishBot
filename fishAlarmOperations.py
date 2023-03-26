import pandas
from datetime import datetime, timezone, timedelta

import pandas as pd
import pytz

# This script will contain an hour offset for fishing friday alarm
def getAlarmInfo(serverName):
    df = getTimezoneData(serverName)

def getCurrentTimeUTC():
    return datetime.now(timezone.utc)

def getCurrentTime(serverID):
    """
    :param int serverID:
    :return:

    Insert a server that has an entry in the serverTimezones table to receive the localized time.
    If the server does not have an set timezone, this function will return False.
    """
    df = getTimezoneData()
    UTCTime = getCurrentTimeUTC()
    selectedServer = df[df['serverID'] == serverID]

    try:
        timezoneAdjust = UTCTime.astimezone(pytz.timezone(selectedServer['timezone'][selectedServer.index[0]]))
    except KeyError:
        return False
    return timezoneAdjust

def storeTimeZone(serverID, timezoneName):
    """
    :param serverID:
    :param string timezoneName:
    :return: none

    This function will save a timezone to a server. When calling the function, include the name of the server, and the name of the timezone.
    You can get the name of the timezone from fishAlarmOperations.convertHourOffset.
    """
    df = getTimezoneData()
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, timezoneName]

        df.loc[selectedServer.index] = [serverID, timezoneName]

    except (ValueError, KeyError):
        data = {"serverID": [serverID],
                "timezone": [timezoneName]}
        df = pd.DataFrame(data)

    df.to_json("serverTimezones.json")

def setFishingFridayEnabled(serverID, enabled, channelID):
    """
    :param serverID:
    :param Boolean enabled:
    :param String channelID:

    Will set a server's fishing friday status to the enabled variable, and will set the included channel as the fishing channel.
    """
    df = getFishingFridayData('')
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, enabled, channelID, 0]

        df.loc[selectedServer.index] = [serverID, enabled, channelID, 0]
    except (ValueError, KeyError):
        data = {'serverID': [serverID],
                'enabled': [enabled],
                'channelID': [channelID],
                "fridayStage": [0]}
        df = pd.DataFrame(data)

    df.to_json("enabledServers.json")

def getFishingFridayInfo(serverName):
    """

    :param serverName:
    :return: Boolean enabledStatus

    This function will take a serverName and return if the server has enabled or disabled fishing friday alarms.
    """
    try:
        df = getFishingFridayData("enabledServers.json")
        return df[serverName][0]
    except KeyError:
        df[serverName] = [False]
        df.to_json("enabledServers.json")
        return False

def convertHourOffset(hourOffset):
    """
    :param int hourOffset:
    :return: string timezone

    This function takes a string in the form of an hour offset, such as '+4' or '-3'.
    It then returns a string usable by pytz to convert a datetime.
    """
    df = pandas.read_json("timezones.json")
    return df["timezones"][hourOffset]

def isItFriday(serverID):
    """
    :param serverID:
    :return: boolean isFriday

    This function returns whether or not it is friday in the timezone of the included serverID
    """
    currentTime = getCurrentTime(serverID)
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
def getTimezoneData():
    df = pandas.read_json("serverTimezones.json", dtype={"serverID": "int64"})

    return df

def getFishingFridayData(server):
    """

    :param server: The name that will be used to start a new dataframe if one does not currently exist.
    :return: df of the enabledServers.json file

    This will return a pandas df of the enabledServers.json file.
    If you choose to use '' as the servername instead, it will simply return the file, or inform you that the file does not exist.
    """
    try:
        df = pandas.read_json("enabledServers.json", dtype={"serverID": "int64", "channelID": "int64", "fridayStage": "int64"})
    except ValueError:
        if server == '':
            return pandas.DataFrame()
        df = pandas.DataFrame(["enabledStatus"], columns=[server])

    return df

def checkAfterHour(serverID, targetHour):
    timestamp = getCurrentTime(serverID)

    if timestamp.hour > targetHour:
        return True
    return False

def incrementStage(serverID):
    df = getFishingFridayData('')
    selectedServer = df[df["serverID"] == serverID]
    currentStage = selectedServer["fridayStage"][selectedServer.index[0]]
    df.at[selectedServer.index[0], 'fridayStage'] = currentStage + 1
    df.to_json("enabledServers.json")

def resetStage(serverID):
    df = getFishingFridayData('')
    selectedServer = df[df["serverID"] == serverID]
    df.at[selectedServer.index[0], 'fridayStage'] = 0
    df.to_json("enabledServers.json")

def getFridayEnabledList():
    """
    :return: list of server ID

    This function will return a dataframe of all server IDs and channel ID's from servers that have fishing friday activated
    """
    df = getFishingFridayData('')
    if df.empty:
        return []

    newDF = df[df['enabled']]
    return newDF
