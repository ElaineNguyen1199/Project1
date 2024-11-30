class Account:
    def __init__(self, name, balance=0):
        self.__account_name = name
        self.__account_balance = 0
        self.set_balance(balance)

    def deposit(self, amount):
        if amount > 0:
            self.__account_balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__account_balance:
            self.__account_balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.__account_balance

    def get_name(self):
        return self.__account_name

    def set_balance(self, value):
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value):
        self.__account_name = value

    def __str__(self):
        return f'Account name = {self.__account_name}, Account balance = {self.__account_balance:.2f}'
