from abc import ABC, abstractmethod

from investments.date import Date


class Ticker(ABC):
    @abstractmethod
    def getPriceOn(self, date: Date):
        pass
