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
