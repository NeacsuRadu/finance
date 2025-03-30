CASH = "deposit"


class CashOperation:
    def __init__(self, type, amount, timestamp):
        self.type = type
        self.amount = amount
        self.timestamp = timestamp

    def getAmount(self):
        return self.amount

    def getType(self):
        return self.type

    def isBefore(self, timestamp):
        return self.timestamp < timestamp
