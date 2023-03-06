import pandas
from datetime import datetime, timezone
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
    df.to_json("fishAlarmInfo.json")

def convertHourOffset(hourOffset):
    """
    :param int hourOffset:
    :return: string timezone

    This function takes a string in the form of an hour offset, such as '+4' or '-3'.
    It then returns a string usable by pytz to convert a datetime.
    """
    df = pandas.read_json("timezones.json")
    return df["timezones"][hourOffset]

def getJsonData(server):
    try:
        df = pandas.read_json("fishAlarmInfo.json")
    except ValueError:
        df = pandas.DataFrame(["timezone"], columns=[server])

    return df
