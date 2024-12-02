class Account:
    """
    A class that represents a bank account with basic functionalities:
    Deposit, Withdrawal, and balance management.
    """
    def __init__(self, name: str, balance: float =0.0) -> None:
        """
        Initializes an Account object
        :param name: User's account name
        :param balance: The initial balance of the account, the Default is 0.0.
        """
        self.__account_name = name
        self.__account_balance = 0
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposit the amount into the account
        :param amount: The amount to deposit into the account. Must be greater than 0.
        :return: True if the deposit is successful, False otherwise.
        """
        if amount > 0:
            self.__account_balance += amount
            return True
        else:
            return False

    def withdraw(self, amount: float) -> bool:
        """
        withdraws an amount from the account.
        :param amount: The amount to withdraw. Must be greater than 0 and less than or equal to the current balance.
        :return:
        """
        if amount > 0 and amount <= self.__account_balance:
            self.__account_balance -= amount
            return True
        else:
            return False

    def get_balance(self) -> float:
        """
        Gets the current balance of the account.
        :return: The current balance of the account
        """
        return self.__account_balance

    def get_name(self) -> str:
        """
        Gets the name of the account holder
        :return: The name of the account holder
        """
        return self.__account_name

    def set_balance(self, value: float) -> None:
        """
        Sets the balance of the account.
        :param value: The new balance. if the value is negative, the balance is set to 0.
        """
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value: str) -> None:
        """
        sets the name of the account holder.
        :param value: The new name for the account holder.
        """
        self.__account_name = value

    def __str__(self) -> str:
        """
        Returns the output of the Account name and Account balance
        :return: A string that contains the user account name, and balance.
        """
        return f'Account name = {self.__account_name}, Account balance = {self.__account_balance:.2f}'
