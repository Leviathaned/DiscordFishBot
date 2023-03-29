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

def addComment(serverID, comment):
    df = pandas.read_json("fridayComments.json", dtype={"serverID": "int64", "comment": "list"})
    df = df.astype('object')
    try:
        selectedServer = df[df["serverID"] == serverID]

        if selectedServer.empty:
            df.loc[len(df.index)] = [serverID, comment]
            return

        currentComments = selectedServer["comments"].tolist()
        if isinstance(currentComments[0], str):
            currentComments.extend([comment])
        else:
            currentComments[0].extend([comment])
        df.loc[selectedServer.index] = [serverID, currentComments]

    except (ValueError, KeyError):
        data = {"serverID": [serverID],
                "comments": comment}
        df = pd.DataFrame(data)

    df.to_json("fridayComments.json")
