import csv
import random
import pandas

def getFishFactCount(serverName):
    df = pandas.read_json("fishFacts.json")
    fishFacts = df[serverName]
    return len(fishFacts)


def grabFishFact(serverName):
    df = pandas.read_json("fishFacts.json")
    randomFactIndex = random.randint(0, len(df[serverName]) - 1)
    print(df[serverName])
    return str(randomFactIndex + 1) + ') ' + df[serverName][randomFactIndex]


def grabSpecificFishFact(serverName, i):
    df = pandas.read_json("fishFacts.json")
    fishFact = df[serverName][i - 1]
    return str(i) + ') ' + fishFact


def addFishFact(serverName, fishFact):
    df = pandas.read_json("fishFacts.json")
    factCount = getFishFactCount(serverName)
    df[serverName][str(factCount)] = fishFact
    df.to_json(r'fishFacts.json')


def removeFishFact(serverName, index):
    df = pandas.read_json("fishFacts.json")
    factCount = getFishFactCount(serverName)

    # Make this actually signal that the process has failed, and have the bot notify the user of error
    if len(df[serverName]) > index:
        return

    del df[serverName][index - 1]
    df.to_json(r'fishFacts.json')
    return
