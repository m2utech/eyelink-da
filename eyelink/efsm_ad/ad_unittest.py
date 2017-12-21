import unittest
import util
import pytz
import consts
from datetime import datetime
from dateutil.relativedelta import relativedelta

localDate = "2017-11-11T00:00:00Z"
utcDate = "2017-11-10T15:00:00Z"
fm = "%Y-%m-%dT%H:%M:%SZ"

class utilTest(unittest.TestCase):
    def test_getTimezone(self):
        self.assertIn(consts.LOCAL_TIMEZONE, util.getTimezone())

    def test_getToday(self):
        dt = datetime.now(pytz.UTC)
        dt = dt.strftime(fm)
        self.assertEqual(util.getToday(True, fm), dt)

    def test_getLocalStr2Utc(self):
        self.assertEqual(util.getLocalStr2Utc(localDate, fm), utcDate)

    def test_getUtcStr2Local(self):
        self.assertEqual(util.getUtcStr2Local(utcDate, fm), localDate)

    def test_getStartEndDateByHour(self):
        dt = datetime.now(pytz.UTC)
        s_date = (dt - relativedelta(hours=3)).strftime(fm)
        e_date = dt.strftime(fm)
        self.assertEqual(util.getStartEndDateByHour(3,True,fm), (s_date, e_date))
    def test_getStartEndDateByMinute(self):
        dt = datetime.now(pytz.UTC)
        s_date = (dt - relativedelta(minutes=3)).strftime(fm)
        e_date = dt.strftime(fm)
        self.assertEqual(util.getStartEndDateByMinute(3,True,fm), (s_date, e_date))
    def test_getStartEndDateByDay(self):
        dt = datetime.now(pytz.UTC)
        s_date = (dt - relativedelta(days=3)).strftime(fm)
        e_date = dt.strftime(fm)
        self.assertEqual(util.getStartEndDateByDay(3,True,fm), (s_date, e_date))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(utilTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
