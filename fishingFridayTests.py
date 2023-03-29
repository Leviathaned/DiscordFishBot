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

    def testComment(self):
        fishingFridayOperations.addComment(1088123578966360114, "This is a sample comment to be voted upon!", 321724036155441153)
        self.assertEqual(True, True)

    def testUserCommentExists(self):
        exists = fishingFridayOperations.checkIfUserCommentExists(1088123578966360114, 321724036155441153)
        print(exists)
        self.assertEqual(True, True)
