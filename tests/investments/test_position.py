import unittest
from investments.position import Position
from investments.date import Date

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.eunl_position = Position("EUNL.DE")
        self.week_day_date = Date(25,3,2025)
        self.weekend_day_date = Date(23,3,2025)

    def test_getPriceOnReturnsCurrentDayOpenPriceForWeekDays(self):
        self.assertEqual(self.eunl_position.getPriceOn(self.week_day_date), 100.78)
    
    def test_getPriceOnReturnsLastWeekDayClosePriceForWeekendDays(self):
        self.assertEqual(self.eunl_position.getPriceOn(self.weekend_day_date), 98.91)
        
if __name__ == '__main__':
    unittest.main()