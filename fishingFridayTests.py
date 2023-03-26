import unittest
import fishingFridayOperations

class FishingFridayTests(unittest.TestCase):

    def testGrabFishingFridayMessages(self):
        print(fishingFridayOperations.grabFishingFridayMessage())
        self.assertEqual(True, True)