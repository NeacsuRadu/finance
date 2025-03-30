from datetime import datetime, timedelta

class Date:

    def __init__(self, day: int, month: int, year: int):
        self.__datetime = datetime(year=year, month=month, day=day)
    
    def toString(self):
        return self.__datetime.strftime('%Y-%m-%d')
    
    def isWeekDay(self):
        return self.__datetime.weekday() < 5
    
    def getLastWeekDayDate(self):
        if self.__isSaturday():
            one_day_ago = self.__datetime + timedelta(days=-1)
            return Date(day=one_day_ago.day, month=one_day_ago.month, year=one_day_ago.year)

        if self.__isSunday():
            two_days_ago = self.__datetime + timedelta(days=-2)
            return Date(day=two_days_ago.day, month=two_days_ago.month, year=two_days_ago.year)
        
        return Date(day=self.__datetime.day, month=self.__datetime.month, year=self.__datetime.year)

    def __isSaturday(self):
        return self.__datetime.weekday() == 5
    
    def __isSunday(self):
        return self.__datetime.weekday() == 6
    
    def getNextDay(self):
        tomorrow = self.__datetime + timedelta(days=1)
        return Date(day=tomorrow.day, month=tomorrow.month, year=tomorrow.year)
