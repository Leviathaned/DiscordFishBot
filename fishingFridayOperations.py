import traceback

import pandas
import pandas as pd
import random

def fish():
    df = pd.read_json("fishList.json")
    df = df["parse"]["links"]
    return df[random.randint(0, len(df) - 1)]['title']

def grabFishingFridayMessage():
    df = pd.read_json("fishingFridayMessage.json")
    messagesList = df["fridayMessages"].tolist()
    return messagesList[random.randint(0, len(messagesList) - 1)]

def readFactsFile(jsonFile):
    df = pandas.read_json(jsonFile, dtype={"serverID": "int64", "comment": "list", "user": "list"})
    return df

def saveFactsFile(jsonFile, dataframe):
    """

    :param jsonFile:
    :param dataframe:
    :return:
    """
    dataframe.to_json(jsonFile)
    return

def readFishFactData(jsonFile):
    """
    When given a valid jsonFile for friday comments, this function will extract and return a dataframe for use.
    If the jsonFile can't be read for whatever reason, it will return a fresh dataframe.
    :param jsonFile:
    :return: Pandas df:
    """
    try:
        df = pandas.read_json(jsonFile)
    except:
        traceback.print_exc()
        df = pandas.DataFrame()
        print("Unable to read Friday Comments Json! Creating a new dataframe...")
    return df

def saveFridayCommentsData(jsonFile, dataframe):
    """
    :param jsonFile:
    :param dataframe:
    :return:
    """
    dataframe.to_json(jsonFile)

def readFridayCommentsData(jsonFile):
    """
    :param jsonFile:
    :return:
    """
    try:
        df = pandas.read_json(jsonFile)
        if df.empty:
            print("The inserted .json is empty! Creating a new dataframe...")
            df = pandas.DataFrame(columns=["serverID", "comment", "user"])
            return df
        return df
    except:
        traceback.print_exc()
        print("The json could not be read properly! Returning an empty dataframe...")
        df = pandas.DataFrame(columns = ["serverID", "comment", "user"])
        return df

def createFridayCommentsTable(serverID, comment, user):
    data = {"serverID": serverID,
            "comment": comment,
            "user": user}
    df = pd.DataFrame(data)
    return df

def addComment(df, serverID, comment, user):
    """

    :param df:
    :param serverID:
    :param comment:
    :param user:
    :return:

    This function will add a row to the inserted dataframe under the serverID and containing the userID.
    If the user already has a comment, it will replace the pre-existing comment.
    """
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, comment, user]
            print("selected server empty!")
            return df

        currentComments = selectedServer["comment"].tolist()
        currentUsers = selectedServer["user"].tolist()

        # check if comment already exists to be replaced
        for index in range(0, len(currentUsers)):
            if currentUsers[index] == user:
                currentComments[index] = comment
                df.loc[index] = [serverID, comment, user]
                print("Identical comment found!")
                return df

        df.loc[len(df.index)] = [serverID, comment, user]

        return df
    except KeyError:
        traceback.print_exc()
        print("There was an issue with reading the inserted dataframe! Make sure your dataframe is formatted properly!")
        return False

def checkIfUserCommentExists(df, serverID, user):
    """
    :param df:
    :param serverID:
    :param user:
    :return: exists
    This function returns the user's currently submitted comment, and false if the user does not have a comment, or if there is an error reading the dataframe.
    """
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            return False

        currentComments = selectedServer["comment"].tolist()
        currentUsers = selectedServer["user"].tolist()

        for index in range(0, len(currentUsers)):
            if currentUsers[index] == user:
                return currentComments[index]

        return False

    except (ValueError, KeyError):
        traceback.print_exc()
        return False

def clearFridayComments():
    df = pd.DataFrame()
    print(df)
    df.to_json("fridayComments.json")
    return
