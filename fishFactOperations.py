import os
import random
import pandas


def readFishFactData():
    try:
        df = pandas.read_json("fishFacts.json")
    except:
        df = pandas.DataFrame()
        df.to_json("fishFacts.json")
        print("File fishFacts.json not found! Creating new fishFacts.json file.")
        return df


def getFishFactCount(serverName):
    df = readFishFactData()
    fishFacts = df[serverName][0]
    return len(fishFacts)


def grabFishFact(serverName):
    df = readFishFactData()
    randomFactIndex = random.randint(0, len(df[serverName][0]) - 1)
    return str(randomFactIndex + 1) + ') ' + df[serverName][0][str(randomFactIndex)]


def grabSpecificFishFact(serverName, i):
    df = readFishFactData()
    fishFact = df[serverName][0][str(i - 1)]
    return str(i) + ') ' + fishFact


def addFishFact(serverName, fishFact):
    df = readFishFactData()
    try:
        factCount = getFishFactCount(serverName)
        df[serverName][0][str(factCount)] = fishFact
        df.to_json(r'fishFacts.json')
        return
    except KeyError:
        print("Creating new fact table for " + str(serverName))
        df[serverName] = [{"0": fishFact}]
        df.to_json(r'fishFacts.json')


def removeFishFact(serverName, index):
    df = readFishFactData()

    # Make this actually signal that the process has failed, and have the bot notify the user of error
    if len(df[serverName][0]) <= index:
        return

    for i in range(index, len(df[serverName][0])):
        df[serverName][0][str(i - 1)] = df[serverName][0][str(i)]

    del df[serverName][0][str(len(df[serverName][0]) - 1)]
    df.to_json(r'fishFacts.json')
    return
