import fishAlarmOperations
import unittest
import pandas
from datetime import datetime, timezone
import pytz

class FishAlarmTests(unittest.TestCase):

    def testGetAlarmInfo(self):
        fishAlarmOperations.getAlarmInfo("testing")
        self.assertEqual(True, True)

    def testStoreTimeZone(self):
        fishAlarmOperations.storeTimeZone("testing3", "Europe/Berlin")
        self.assertEqual(True, True)

    def testGetAdjustedTime(self):
        print(fishAlarmOperations.getCurrentTime(844663929086935070))
        self.assertEqual(True, True)

    def testGetCurrentTimeWrongName(self):
        self.assertEqual(False, fishAlarmOperations.getCurrentTime("doesNotExist"))

    def testGetAllTimezones(self):
        print(pytz.common_timezones)
        self.assertEqual(True, True)

    def testSaveTimezone(self):
        timezoneName = fishAlarmOperations.convertHourOffset(4)
        self.assertEqual(timezoneName, "Asia/Baku")

    def testTimeZoneAccuracy(self):
        for x in range(-11, 13, 1):
            print(x)
            timezoneName = fishAlarmOperations.convertHourOffset(x)
            UTCTime = datetime.now(timezone.utc)
            timezoneAdjust = UTCTime.astimezone(pytz.timezone(timezoneName))
            print(timezoneAdjust)

    def testGetFishingFridayInfo(self):
        enabled = fishAlarmOperations.getFishingFridayInfo("testing")
        self.assertEqual(enabled, False)

    def testSwitchServerEnabled(self):
        enabled = fishAlarmOperations.getFishingFridayInfo("testing2")
        fishAlarmOperations.switchFishingFridayEnabled("testing2")
        self.assertEqual(not enabled, fishAlarmOperations.getFishingFridayInfo("testing2"))

    def testTimeUntilFriday(self):
        currentTime = fishAlarmOperations.getCurrentTime("Bot Testin")
        duration = fishAlarmOperations.getTimeUntilFriday(currentTime)
        print(duration)
        self.assertEqual(True, True)

    def testGetEnabledServers(self):
        print(fishAlarmOperations.getFridayEnabledList())
        self.assertEqual(True, True)

    def testGetEnabledChannel(self):
        print(fishAlarmOperations.getFridayEnabledChannel('844663929086935070'))
        self.assertEqual(True, True)

    def testSetEnabledServer(self):
        fishAlarmOperations.setFishingFridayEnabled(844663929086935070, True, 844663929837060148)
        self.assertEqual(True, True)

    def testIncrementStage(self):
        fishAlarmOperations.incrementStage(844663929086935070)
        self.assertEqual(True, True)











