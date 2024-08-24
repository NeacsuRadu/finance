class Portofolio:
    
    def __init__(self):
        self.cash = 0
        self.cashOperations = []

    def addDeposit(self, amount):
        self.cashOperations.append(amount)
        self.cash += amount