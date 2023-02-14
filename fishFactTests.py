import fishFactOperations
import unittest

class TestFishFacts(unittest.TestCase):

    def testCountFishFacts(self):
        self.assertEqual(2, fishFactOperations.getFishFactCount("testing"), "There is an error in getFishFactCount!")

    def testGrabFishFact(self):
        fishFact = fishFactOperations.grabFishFact("testing")
        print(fishFact)
        self.assertEqual(fishFact, "1) This is testing fish fact #1!")

    def testGrabSpecificFishFact(self):
        fishFact = fishFactOperations.grabSpecificFishFact("testing2", 2)
        print(fishFact)
        self.assertEqual(fishFact, "2) This is testing fish fact #2 from the second test server!")

    def testAddAndRemove(self):
        fishFactOperations.addFishFact("testing", "Hello, and welcome to the next sample fish fact!")
        fishFactOperations.removeFishFact("testing", 2)
        self.assertEqual(2, fishFactOperations.getFishFactCount("testing"), "There is an error in getFishFactCount!")
