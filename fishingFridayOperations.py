import pandas as pd
import random

def fish():
    df = pd.read_json("fishPrizes.json")

def grabFishingFridayMessage():
    df = pd.read_json("fishingFridayMessage.json")
    messagesList = df["fridayMessages"].tolist()
    return messagesList[random.randint(0, len(messagesList) - 1)]
