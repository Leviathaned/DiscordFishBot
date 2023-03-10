import pandas
from datetime import datetime, timezone, timedelta
import pytz

# This script will contain an hour offset for fishing friday alarm
def getAlarmInfo(serverName):
    df = getJsonData(serverName)
    print(df)

def getCurrentTimeUTC():
    return datetime.now(timezone.utc)

def getCurrentTime(serverName):
    """
    :param string serverName:
    :return:

    Insert a server that has an entry in the alarmInfo table to receive the localized time.
    If the server does not have an entry, this function will return False.
    """
    df = getJsonData(serverName)
    UTCTime = getCurrentTimeUTC()

    try:
        timezoneAdjust = UTCTime.astimezone(pytz.timezone(df[serverName][0]))
    except KeyError:
        return False
    return timezoneAdjust

def storeTimeZone(serverName, timezoneName):
    """
    :param string serverName:
    :param string timezoneName:
    :return: none

    This function will save a timezone to a server. When calling the function, include the name of the server, and the name of the timezone.
    You can get the name of the timezone from fishAlarmOperations.convertHourOffset.
    """
    df = getJsonData(serverName)
    df[serverName] = [timezoneName]
    df.to_json("serverTimezones.json")

def setFishingFridayEnabled(serverID, enabled):
    """
    :param String serverID:
    :param Boolean enabled:

    Will set a server's fishing friday status to the enabled variable.
    """
    df = getFishingFridayData(serverID)
    df[serverID] = [enabled]
    df.to_json("enabledServers.json")

def switchFishingFridayEnabled(serverName):
    """
    :param String serverName:
    :return: Boolean enabledStatus

    This function will take a server name and switch the fishing friday alerts enabled status.
    It will then return if the status has been set to enabled or disabled.
    """

    enabledStatus = not (getFishingFridayInfo(serverName))

    df = getFishingFridayData(serverName)
    df[serverName] = [enabledStatus]
    df.to_json("enabledServers.json")

    return enabledStatus

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
        print("creating a new column")
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

def isItFriday(serverName):
    currentTime = getCurrentTime(serverName)
    if currentTime.weekday() == 4:
        return True
    return False

def getTimeUntilFriday(currentTime):
    """

    :param datetime currentTime:
    :return: duration

    This function takes a datetime, and returns the duration until it is friday.
    It will return True if it is already friday.
    """
    currentDay = ((currentTime.weekday() + 2) % 7)
    if currentDay == 6:
        return True

    goalTime = currentTime + timedelta(hours = (6 - currentDay) * 24)
    goalTime = goalTime.replace(hour=0, minute=0, second=0, microsecond=0)
    return goalTime - currentTime

# functions to get json data into a df that check if the file exists
def getJsonData(server):
    try:
        df = pandas.read_json("serverTimezones.json")
    except ValueError:
        df = pandas.DataFrame(["timezone"], columns=[server])

    return df

def getFishingFridayData(server):
    try:
        df = pandas.read_json("enabledServers.json")
    except ValueError:
        df = pandas.DataFrame(["enabledStatus"], columns=[server])

    return df
