import os
import random
import traceback

import pandas


def readFishFactData(jsonFile):
    try:
        df = pandas.read_json(jsonFile)
    except:
        traceback.print_exc()
        df = pandas.DataFrame()
        print("Unable to read fish fact table! Creating a new dataframe...")

    return df

def saveFishFactData(fishFactDf, jsonFile):
    fishFactDf.to_json(jsonFile)
    return

def getFishFactCount(fishFactDf, serverName):
    fishFacts = fishFactDf[serverName][0]
    return len(fishFacts)

def grabFishFact(fishFactDf, serverName):
    print(fishFactDf)
    randomFactIndex = random.randint(0, len(fishFactDf[serverName][0]) - 1)
    return str(randomFactIndex + 1) + ') ' + fishFactDf[serverName][0][str(randomFactIndex)]


def grabSpecificFishFact(fishFactDf, serverName, i):
    fishFact = fishFactDf[serverName][0][str(i - 1)]
    return str(i) + ') ' + fishFact


def addFishFact(fishFactDf, serverName, fishFact):
    factCount = getFishFactCount(fishFactDf, serverName)
    fishFactDf[serverName][0][str(factCount)] = fishFact
    return fishFactDf

def removeFishFact(fishFactsDf, serverName, index):
    # Make this actually signal that the process has failed, and have the bot notify the user of error
    if len(fishFactsDf[serverName][0]) + 1 <= index:
        return False

    for i in range(index, len(fishFactsDf[serverName][0])):
        fishFactsDf[serverName][0][str(i - 1)] = fishFactsDf[serverName][0][str(i)]

    del fishFactsDf[serverName][0][str(len(fishFactsDf[serverName][0]) - 1)]
    return fishFactsDf
