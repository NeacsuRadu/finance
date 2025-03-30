import unittest

from investments.date import Date


class TestDate(unittest.TestCase):
    def test_toString(self):
        d = Date(24, 3, 2025)
        self.assertEqual(d.toString(), '2025-03-24')
    
    def test_isWeekDayReturnsTrueForWeekDay(self):
        d = Date(24, 3, 2025)
        self.assertTrue(d.isWeekDay())
    
    def test_isWeekDayReturnsFalseForWeekendDay(self):
        d = Date(23, 3, 2025)
        self.assertFalse(d.isWeekDay())
    
    def test_getLastWeekDayDateReturnsFridayIfSaturday(self):
        d = Date(29, 3, 2025)
        self.assertEqual(d.getLastWeekDayDate().toString(), '2025-03-28')

    def test_getLastWeekDayDateReturnsFridayIfSunday(self):
        d = Date(23, 3, 2025)
        self.assertEqual(d.getLastWeekDayDate().toString(), '2025-03-21')

    def test_getLastWeekDayDateReturnsCurrentDayIfWeekDay(self):
        d = Date(24, 3, 2025)
        self.assertEqual(d.getLastWeekDayDate().toString(), '2025-03-24')
    
    def test_getNextDay(self):
        d = Date(24, 3, 2025)
        self.assertEqual(d.getNextDay().toString(), '2025-03-25')

if __name__ == '__main__':
    unittest.main()
