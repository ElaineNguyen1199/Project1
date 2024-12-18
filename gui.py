from tkinter import *
from tkinter import messagebox
from logic import *
import csv
import os

class AccountGUI:
    def __init__(self, window):
        """
        Creates the AccountGUI with the main Tkinter window and sets up the login interface
        :param window: The main Tkinter window for the application
        """
        self.window = window

        Label(self.window, text="ATM").pack(pady=10)
        frame_first_name = Frame(self.window)
        Label(frame_first_name, text="First Name:").pack(side=LEFT, padx=5)
        self.first_name_entry = Entry(frame_first_name)
        self.first_name_entry.pack(side=LEFT, padx=5)
        frame_first_name.pack(pady=5)

        frame_last_name = Frame(self.window)
        Label(frame_last_name, text="Last Name:").pack(side=LEFT, padx=5)
        self.last_name_entry = Entry(frame_last_name)
        self.last_name_entry.pack(side=LEFT, padx=5)
        frame_last_name.pack(pady=5)

        frame_pin = Frame(self.window)
        Label(frame_pin, text="Enter PIN:").pack(side=LEFT, padx=5)
        self.pin_entry = Entry(frame_pin, show="*")  # Hides user input with *
        self.pin_entry.pack(side=LEFT, padx=5)
        frame_pin.pack(pady=5)

        self.search_button = Button(self.window, text="Search", command=self.handle_login)
        self.search_button.pack(pady=10)

        self.message_label = Label(self.window, text="")
        self.message_label.pack(pady=10)

        self.withdraw_var = BooleanVar()
        self.deposit_var = BooleanVar()
        self.amount_entry = None
        self.account = None

    def handle_login(self) -> None:
        """
        Manages the login or account creation process. Verifies user inputs and can load an existing account or create
        a new one if not found.
        :return: None (explicitly or exits early if input validation fails.)
        """
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not first_name or not last_name or not pin.isdigit():
            messagebox.showerror("Error", "Please enter valid details.")
            return

        account_name = f"{first_name} {last_name}"
        if self.load_account(account_name, pin):
            self.message_label.config(text=f"Welcome, {first_name} {last_name}!")
            self.display_account_options()
        else:
            if messagebox.askyesno("New Account", "Account not found. Would you like to create one?"):
                self.account = Account(account_name)
                self.save_account(account_name, pin, 0)
                self.message_label.config(text=f"Welcome, {first_name}!")
                self.display_account_options()

    def display_account_options(self) -> None:
        """
        Displays the account options withdraw and deposit button and shows the current account balance.
        """
        Label(self.window, text="What would you like to do?").pack(pady=10)

        frame_radio_buttons = Frame(self.window)
        Radiobutton(frame_radio_buttons, text="Withdraw", variable=self.withdraw_var, value=True).pack(side=LEFT, padx=10)
        Radiobutton(frame_radio_buttons, text="Deposit", variable=self.withdraw_var, value=False).pack(side=LEFT, padx=10)
        frame_radio_buttons.pack(pady=5)

        frame_amount = Frame(self.window)
        Label(frame_amount, text="Amount:").pack(side=LEFT, padx=5)
        self.amount_entry = Entry(frame_amount)
        self.amount_entry.pack(side=LEFT, padx=5)
        frame_amount.pack(pady=10)

        frame_buttons = Frame(self.window)
        Button(frame_buttons, text="Enter", command=self.handle_transaction).pack(side=LEFT, padx=10)
        Button(frame_buttons, text="Exit", command=self.window.quit).pack(side = LEFT, padx=10)
        frame_buttons.pack(pady = 10)

        self.balance_label = (Label(self.window, text=f"Your account balance is: ${self.account.get_balance():.2f}"))
        self.balance_label.pack(pady =10)

    def handle_transaction(self) -> None:
        """
        Processes the users transaction from either withdrawing or depositing and updates the account balance.
        """
        try:
            amount = float(self.amount_entry.get())
            if self.withdraw_var.get():
                success = self.account.withdraw(amount)
                action = "Withdraw"
            else:
                success = self.account.deposit(amount)
                action = "Deposit"

            if success:
                self.save_account(self.account.get_name(), self.pin_entry.get(), self.account.get_balance())
                self.balance_label.config(text=f"Your account balance is: ${self.account.get_balance():.2f}")
                messagebox.showinfo("Success", f"{action} successful! New balance: ${self.account.get_balance():.2f}")
            else:
                messagebox.showerror("Error", f"{action} failed. Check balance or amount.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def save_account(self, name: str, pin: int, balance: float) -> None:
        """
        writes the user account information to a CSV file.
        :param name: User's account name
        :param pin: User's Pin
        :param balance: User's account balance
        """
        file_exists = os.path.isfile("ATM.csv")
        with open("ATM.csv", mode="a", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONE)
            if not file_exists:
                writer.writerow(["Name", "Pin", "Balance"])
            writer.writerow([name, pin, f'${balance:.2f}'])

    def load_account(self, name: str, pin: int) -> bool:
        """
        Loads the account details from the CSV file.
        :param name: User's account name
        :param pin: User's pin
        :return: True or False if the account has been found or not been found.
        """
        try:
            with open("ATM.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[0] == name and row[1] == pin:
                        balance = float(row[2].replace("$", "").strip()) #This helps not get an error saying can't convert string to into float because of the $
                        self.account = Account(name, balance)
                        return True
            return False
        except FileNotFoundError:
            return False