import pandas

import unittest
import fishingFridayOperations

class FishingFridayTests(unittest.TestCase):

    def testGrabFishingFridayMessages(self):
        print(fishingFridayOperations.grabFishingFridayMessage())
        self.assertEqual(True, True)

    def testFish(self):
        fish = fishingFridayOperations.fish()
        print(fish)
        fish = fish.replace(" ", "_")
        print("https://en.wikipedia.org/wiki/" + fish)
        self.assertEqual(True, True)

    def testAddComment(self):
        data1 = {
            "serverID": ["fishFactTesting", "fishFactTesting"], "comment": ["This is my extremely cool comment!", "This is my less cool comment"], "user": ["sampleUser1", "sampleUser2"]
        }
        data2 = {
            "serverID": ["fishFactTesting"], "comment": ["This is my extremely cool comment!"], "user": ["sampleUser1"]
        }
        df1 = pandas.DataFrame(data1)
        df2 = pandas.DataFrame(data2)

        df2 = fishingFridayOperations.addComment(df2, "fishFactTesting", "This is my less cool comment", "sampleUser2")

        self.assertEqual(True, pandas.DataFrame.equals(df1, df2))

    def testAddCommentKeyError(self):
        data1 = {
            "server": ["This is a purposely bad dataframe."], "Comment": ["This datafrmae cannot be used."], "user": ["woohootestCase"]
        }
        df1 = pandas.DataFrame(data1)
        df1 = fishingFridayOperations.addComment(df1, "fishFactTesting", "This should NOT work!", "sampleUser2")

        self.assertEqual(df1, False)

    def testAddSeveralComments(self):
        data1 = {
            "serverID": ["fishTestingServer", "fishUsingServer", "fishTestingServer", "fishTestingServer", "fishUsingServer"],
            "comment": ["Cool comment!", "Adding more comments!", "A third comment!", "fourth, even?", "A sus comment..."],
            "user": ["sampleUser1", "sampleUser2", "sampleUser2", "sampleUser3", "sampleUser1"]
        }
        data2 = {
            "serverID": ["fishTestingServer", "fishUsingServer"],
            "comment": ["Cool comment!", "Adding more comments!"],
            "user": ["sampleUser1", "sampleUser2"]
        }
        df1 = pandas.DataFrame(data1)
        df2 = pandas.DataFrame(data2)

        df2 = fishingFridayOperations.addComment(df2, "fishTestingServer", "A third comment!", "sampleUser2")
        df2 = fishingFridayOperations.addComment(df2, "fishTestingServer", "fourth, even?", "sampleUser3")
        df2 = fishingFridayOperations.addComment(df2, "fishUsingServer", "A sus comment...", "sampleUser1")

        print("Dataframe 1:")
        print(df1)
        print("Dataframe 2:")
        print(df2)

        self.assertEqual(True, pandas.DataFrame.equals(df1, df2))

    def testReplaceComment(self):
        data1 = {
            "serverID": ["fishTestingServer", "fishTestingServer"], "comment": ["I am the better comment!", "I am an additional comment"], "user": ["sampleUser1", "sampleUser2"]
        }
        data2 = {
            "serverID": ["fishTestingServer", "fishTestingServer"], "comment": ["I am the worse comment...", "I am an additional comment"], "user": ["sampleUser1", "sampleUser2"]
        }
        df1 = pandas.DataFrame(data1)
        df2 = pandas.DataFrame(data2)

        df2 = fishingFridayOperations.addComment(df2, "fishTestingServer", "I am the better comment!", "sampleUser1")

        print(df1)
        print(df2)

        self.assertEqual(True, pandas.DataFrame.equals(df1, df2))

    def testCommentAlreadyExists(self):
        data1 = {
            "serverID": ["testFishingServer"], "comment": ["This is the existing comment."], "user": ["sampleUser1"]
        }
        df1 = pandas.DataFrame(data1)

        self.assertEqual("This is the existing comment.", fishingFridayOperations.checkIfUserCommentExists(df1, "testFishingServer", "sampleUser1"))

    def testCommentDoesNotExist(self):
        data1 = {
            "serverID": ["testFishingServer"], "comment": ["This is the existing comment"], "user": ["sampleUser1"]
        }
        df1 = pandas.DataFrame(data1)
        self.assertEqual(False, fishingFridayOperations.checkIfUserCommentExists(df1, "testFishingServer", "sampleUser2"))