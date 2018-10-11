class Account:
    counter = 0

    def __init__(self, name, ini_bal):
        self.owner = name
        self.balance = ini_bal
        Account.counter += 1

    def deposit(self, amount):
        self.balance = self.balance + amount

    def printbal(self):
        print(self.balance)

    def print_acc(self):
        outputline='''Account owner: %s 
        Account balance: %s''' % (self.owner, self.balance)
        return outputline

    def accountinstances():
        return Account.counter

    def __del__(self):
        Account.counter -= 1


acc_1 = Account('Tom', 100)
acc_2 = Account('Jerry', 300)
acc_3 = Account('William', 500)
print(Account.accountinstances())
del(acc_1)
print(Account.accountinstances())