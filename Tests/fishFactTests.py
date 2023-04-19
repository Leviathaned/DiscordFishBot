import pandas

import fishFactOperations
import unittest

class TestFishFacts(unittest.TestCase):

    def testAddFishFact(self):
        data1 = {
            "fishFactTesting": [{"0": "I really love fishing!"}]
        }

        data2 = {
            "fishFactTesting": [{"0": "I really love fishing!", "1": "Fishing is the coolest!"}]
        }
        df1 = pandas.DataFrame(data1)
        df2 = pandas.DataFrame(data2)

        df1 = fishFactOperations.addFishFact(df1, "fishFactTesting", "Fishing is the coolest!")
        self.assertEqual(True, pandas.DataFrame.equals(df1, df2))

    def testRemoveFishFact(self):
        data1 = {
            "fishFactTesting": [{"0": "I really love fishing!"}]
        }

        data2 = {
            "fishFactTesting": [{"0": "I really love fishing!", "1": "Fishing is the coolest!"}]
        }
        df1 = pandas.DataFrame(data1)
        df2 = pandas.DataFrame(data2)

        df2 = fishFactOperations.removeFishFact(df2, "fishFactTesting", 2)
        self.assertEqual(True, pandas.DataFrame.equals(df1, df2))

    def testGrabFishFact(self):
        data1 = {
            "fishFactTesting": [{"0": "I really love fishing!"}]
        }
        df1 = pandas.DataFrame(data1)

        fishFact = fishFactOperations.grabFishFact(df1, "fishFactTesting")
        self.assertEqual(fishFact, "1) I really love fishing!")

    def testGrabSpecificFishFact(self):
        data2 = {
            "fishFactTesting": [{"0": "I really love fishing!", "1": "Fishing is the coolest!"}]
        }
        df2 = pandas.DataFrame(data2)

        fishFact = fishFactOperations.grabSpecificFishFact(df2, "fishFactTesting", 2)
        self.assertEqual(fishFact, "2) Fishing is the coolest!")



