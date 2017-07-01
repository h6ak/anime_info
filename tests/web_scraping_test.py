import unittest
import datetime as dt

from anime_info import web_scraping as ws


class TestWebScraping(unittest.TestCase):
    def test_parse_date_1(self):
        date_str = '2017年7月3日(月)23:35～'
        actual = ws.AkibaSoukenInfo._parse_datetime(date_str)
        expected = dt.datetime(2017, 7, 3, 23, 35)
        self.assertEqual(expected, actual)

    def test_parse_date_2(self):
        date_str = '2017年7月3日(月)25:35～'
        actual = ws.AkibaSoukenInfo._parse_datetime(date_str)
        expected = dt.datetime(2017, 7, 4, 1, 35)
        self.assertEqual(expected, actual)

    def test_parse_date_3(self):
        date_str = '2017年7月3日(月)～'
        actual = ws.AkibaSoukenInfo._parse_datetime(date_str)
        expected = dt.datetime(2017, 7, 3, 0, 0)
        self.assertEqual(expected, actual)

    def test_parse_date_4(self):
        date_str = '2017年7月夏～'
        actual = ws.AkibaSoukenInfo._parse_datetime(date_str)
        self.assertEqual(None, actual)

if __name__ == '__main__':
    unittest.main(verbosity=2)
