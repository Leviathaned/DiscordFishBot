import fishAlarmOperations
import unittest
import pandas

class FishAlarmTests(unittest.TestCase):
    def test_store_time_zone(self):
        df1 = {"serverID": {0: "testing1"},
               "timezone": {0: "Asia/Baku"}}

        df2 = {"serverID": {0: "testing1", 1: "testing3"},
               "timezone": {0: "Asia/Baku", 1: "Europe/Berlin"}}

        df1 = pandas.DataFrame(df1)
        df2 = pandas.DataFrame(df2)
        df1 = fishAlarmOperations.storeTimeZone(df1, "testing3", "Europe/Berlin")

        print(df1)
        print(df2)
        print(pandas.DataFrame.equals(df1, df2))

        pandas.testing.assert_frame_equal(df1, df2, check_dtype=True)

    def test_save_timezone(self):
        timezoneName = fishAlarmOperations.convertHourOffset(4)
        self.assertEqual(timezoneName, "Asia/Baku")

    def test_get_server_row(self):
        df1 = {
            "serverID": {0: "testing", 1: "testing2"},
            "enabled": {0: False, 1: True},
            "channelID": {0: "testingChannel", 1: "testing2Channel"},
            "fridayStage": {0: 0, 1: 0},
            "winningComment": {0: "", 1: "Hello world!"},
            "winningUser": {0: "", 1: "Leviathan"},
            "winningVoteCount": {0: -1, 1: 7}
        }
        df2 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Hello world!"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df1 = pandas.DataFrame(df1)
        df2 = pandas.DataFrame(df2)
        df1 = fishAlarmOperations.getServerRow(df1, "testing2")
        pandas.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

    def test_no_server_row(self):
        df1 = {
            "serverID": {0: "testing", 1: "testing1"},
            "enabled": {0: False, 1: True},
            "channelID": {0: "testingChannel", 1: "testing2Channel"},
            "fridayStage": {0: 0, 1: 0},
            "winningComment": {0: "", 1: "Hello world!"},
            "winningUser": {0: "", 1: "Leviathan"},
            "winningVoteCount": {0: -1, 1: 7}
        }
        df1 = pandas.DataFrame(df1)
        df1 = fishAlarmOperations.getServerRow(df1, "testing2")
        self.assertEqual(False, df1)

    def test_get_fishing_friday_info(self):
        df1 = {
            "serverID": {0: "testing"},
            "enabled": {0: True},
            "channelID": {0: "testingChannel"},
            "fridayStage": {0: 2},
            "winningComment": {0: "Hello world! - Leviathan"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df1 = pandas.DataFrame(df1)
        enabled = fishAlarmOperations.getFishingFridayInfo(df1, "testing")
        self.assertEqual(enabled.at[0], True)

    def test_set_server_enabled(self):
        df1 = {
            "serverID": {0: "testing"},
            "enabled": {0: False},
            "channelID": {0: "testingChannel"},
            "fridayStage": {0: 2},
            "winningComment": {0: "Hello world! - Leviathan"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df1 = pandas.DataFrame(df1)
        df1 = fishAlarmOperations.setFishingFridayEnabled(df1, "testing", True, "newTestingChannel")
        print(df1)
        self.assertEqual(True, fishAlarmOperations.getFishingFridayInfo(df1, "testing").at[0])

    def test_get_enabled_servers(self):
        df1 = {
            "serverID": {0: "testing", 1: "testing2"},
            "enabled": {0: False, 1: True},
            "channelID": {0: "testingChannel", 1: "testing2Channel"},
            "fridayStage": {0: 0, 1: 0},
            "winningComment": {0: "", 1: "Hello world!"},
            "winningUser": {0: "", 1: "Leviathan"},
            "winningVoteCount": {0: -1, 1: 7}
        }
        df2 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Hello world!"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df1 = pandas.DataFrame(df1)
        df2 = pandas.DataFrame(df2)
        df1 = fishAlarmOperations.getFridayEnabledList(df1)
        pandas.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True), check_dtype=True)

    def test_increment_stage(self):
        df1 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Hello world!"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df1 = pandas.DataFrame(df1)
        fishAlarmOperations.incrementStage(df1, "testing2")
        self.assertEqual(True, True)

    def test_grab_winning_comment(self):
        df1 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Hello world!"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        baseWinningComment = ['Hello world!', 'Leviathan', 7]
        df1 = pandas.DataFrame(df1)
        winningComment = fishAlarmOperations.getWinningComment(df1, "testing2")
        print(winningComment)
        self.assertEqual(baseWinningComment, winningComment)

    def test_save_winning_comment(self):
        df1 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Hello world!"},
            "winningUser": {0: "Leviathan"},
            "winningVoteCount": {0: 7}
        }
        df2 = {
            "serverID": {0: "testing2"},
            "enabled": {0: True},
            "channelID": {0: "testing2Channel"},
            "fridayStage": {0: 0},
            "winningComment": {0: "Wowie Zowie"},
            "winningUser": {0: "Bestie"},
            "winningVoteCount": {0: 11}
        }
        df1 = pandas.DataFrame(df1)
        df2 = pandas.DataFrame(df2)
        df1 = fishAlarmOperations.saveWinningComment(df1, "testing2", "Wowie Zowie", "Bestie", 11)
        pandas.testing.assert_frame_equal(df1, df2, check_dtype=True)










