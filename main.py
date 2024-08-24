from investments.portofolio import Portofolio

def main():
    p = Portofolio()
    p.addDeposit(123)
    p.addDeposit(413)
    print(p.cash)
    print(p.cashOperations)

if __name__ == "__main__":
    main()