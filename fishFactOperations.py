import os
import random
import pandas


def getFishFactCount(serverName):
    basePath = os.path.dirname(os.path.abspath(__file__))
    df = pandas.read_json(basePath + r'/fishFacts.json')
    fishFacts = df[serverName][0]
    return len(fishFacts)


def grabFishFact(serverName):
    basePath = os.path.dirname(os.path.abspath(__file__))
    df = pandas.read_json(os.path.join(basePath, 'fishFacts.json'))
    randomFactIndex = random.randint(0, len(df[serverName][0]) - 1)
    return str(randomFactIndex + 1) + ') ' + df[serverName][0][str(randomFactIndex)]


def grabSpecificFishFact(serverName, i):
    basePath = os.path.dirname(os.path.abspath(__file__))
    df = pandas.read_json(basePath + r'/fishFacts.json')
    fishFact = df[serverName][0][str(i - 1)]
    return str(i) + ') ' + fishFact


def addFishFact(serverName, fishFact):
    basePath = os.path.dirname(os.path.abspath(__file__))
    df = pandas.read_json(basePath + r'/fishFacts.json')
    factCount = getFishFactCount(serverName)
    df[serverName][0][str(factCount)] = fishFact
    df.to_json(r'fishFacts.json')


def removeFishFact(serverName, index):

    basePath = os.path.dirname(os.path.abspath(__file__))
    df = pandas.read_json(basePath + r'/fishFacts.json')

    # Make this actually signal that the process has failed, and have the bot notify the user of error
    if len(df[serverName][0]) > index:
        return

    del df[serverName][0][str(index - 1)]
    df.to_json(r'fishFacts.json')
    return
