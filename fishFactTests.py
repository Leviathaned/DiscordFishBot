import fishFactOperations
import unittest

class TestFishFacts(unittest.TestCase):

    def testCountFishFacts(self):
        self.assertEqual(1, fishFactOperations.getFishFactCount("testing"), "There is an error in getFishFactCount!")

    def testGrabFishFact(self):
        fishFact = fishFactOperations.grabFishFact("testing")
        self.assertEqual(fishFact, "1) This is testing fish fact #1!")

    def testGrabSpecificFishFact(self):
        fishFact = fishFactOperations.grabSpecificFishFact("testing2", 2)
        self.assertEqual(fishFact, "2) This is testing fish fact #2 from the second test server!")

    def testAddAndRemove(self):
        fishFactOperations.addFishFact("testing2", "Hello, and welcome to the next sample fish fact!")
        fishFactOperations.removeFishFact("testing2", 3)
        self.assertEqual(2, fishFactOperations.getFishFactCount("testing2"), "There is an error in getFishFactCount!")
