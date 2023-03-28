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
