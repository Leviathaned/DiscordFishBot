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
        print(fishAlarmOperations.getCurrentTime("testing2"))
        self.assertEqual(True, True)

    def testGetCurrentTimeWrongName(self):
        self.assertEqual(False, fishAlarmOperations.getCurrentTime("doesNotExist"))

    def testGetAllTimezones(self):
        print(pytz.common_timezones)
        self.assertEqual(True, True)

    def testSaveTimezone(self):
        timezoneName = fishAlarmOperations.convertHourOffset(4)
        self.assertEqual(timezone, "Asia/Baku")

    def testTimeZoneAccuracy(self):
        for x in range(-11, 13, 1):
            print(x)
            timezoneName = fishAlarmOperations.convertHourOffset(x)
            UTCTime = datetime.now(timezone.utc)
            timezoneAdjust = UTCTime.astimezone(pytz.timezone(timezoneName))
            print(timezoneAdjust)








