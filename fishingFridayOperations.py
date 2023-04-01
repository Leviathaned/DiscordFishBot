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

def getFridayComments():
    df = pandas.read_json("fridayComments.json", dtype={"serverID": "int64", "comment": "list", "user": "list"})
    df = df.astype('object')
    return df

def createFridayCommentsTable(serverID, comment, user):
    data = {"serverID": [serverID],
            "comments": comment,
            "user": user}
    df = pd.DataFrame(data)
    return df

def addComment(serverID, comment, user):
    """

    :param serverID:
    :param comment:
    :param user:
    :return:

    This function will add a row to the fridayComments.json under the serverID and containing the userID.
    If the user already has a comment, it will replace the pre-existing comment.
    """
    try:
        df = getFridayComments()
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, [comment], [user]]
            df.to_json("fridayComments.json")
            return

        currentComments = selectedServer["comments"].tolist()[0]
        currentUsers = selectedServer["user"].tolist()[0]

        # check if comment already exists to be replaced
        for index in range(0, len(currentUsers)):
            if currentUsers[index] == user:
                currentComments[index] = comment
                df.loc[selectedServer.index] = [serverID, currentComments, currentUsers]
                df.to_json("fridayComments.json")
                return

        if isinstance(currentComments[0], str):
            currentComments.extend([comment])
            currentUsers.extend([user])
        else:
            currentComments[0].extend([comment])
            currentUsers[0].extend([user])

        df.loc[selectedServer.index] = [serverID, currentComments, currentUsers]

    except (ValueError, KeyError):
        traceback.print_exc()
        commentList = [[comment]]
        userList = [[user]]
        df = createFridayCommentsTable(serverID, commentList, userList)

    df.to_json("fridayComments.json")

def checkIfUserCommentExists(serverID, user):
    """
    :param serverID:
    :param user:
    :return: exists
    This function returns the user's currently submitted comment, and false if the user does not have a comment.
    """
    try:
        df = getFridayComments()
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            return False

        currentComments = selectedServer["comments"].tolist()[0]
        currentUsers = selectedServer["user"].tolist()[0]

        for index in range(0, len(currentUsers)):
            if currentUsers[index] == user:
                return currentComments[index]

        return False

    except (ValueError, KeyError):
        traceback.print_exc()
        return False

def getFridayCommentsDf():
    try:
        df = getFridayComments()
        return df
    except:
        return False

def clearFridayComments():
    df = pd.DataFrame()
    print(df)
    df.to_json("fridayComments.json")
    return
