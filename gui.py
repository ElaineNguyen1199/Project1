import tkinter as tk
#from tkinter import *
from tkinter import messagebox
from main import Account
import csv
import os

class AccountGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ATM")
        self.window.geometry('300x400')
        self.window.resizable(False, False)

        # Input boxes and labels
        tk.Label(self.window, text="First Name:").grid(row=0, column=0, pady=5)
        self.first_name_entry = tk.Entry(self.window)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Last Name:").grid(row=1, column=0, pady=5)
        self.last_name_entry = tk.Entry(self.window)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Enter PIN:").grid(row=2, column=0, pady=5)
        self.pin_entry = tk.Entry(self.window, show="*") #This allows you to hide the users inputs with a *
        self.pin_entry.grid(row=2, column=1)

        self.enter_button = tk.Button(self.window, text="Enter", command=self.handle_login)
        self.enter_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.message_label = tk.Label(self.window, text="")
        self.message_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.withdraw_var = tk.BooleanVar()
        self.deposit_var = tk.BooleanVar()
        self.amount_entry = None
        self.account = None
        self.window.mainloop()

    def handle_login(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not first_name or not last_name or not pin.isdigit():
            messagebox.showerror("Error", "Please enter valid details.")
            return

        # Checks to see if the account already exists
        account_name = f"{first_name} {last_name}"
        if self.load_account(account_name, pin):
            self.message_label.config(text=f"Welcome, {first_name}!")
            self.display_account_options()
        else:
            if messagebox.askyesno("New Account", "Account not found. Would you like to create one?"):
                self.account = Account(account_name)
                self.save_account(account_name, pin, 0)
                self.message_label.config(text=f"Welcome, {first_name}!")
                self.display_account_options()

    def display_account_options(self):
        tk.Label(self.window, text="What would you like to do?").grid(row=5, column=0, columnspan=2, pady=10)

        tk.Radiobutton(self.window, text="Withdraw", variable=self.withdraw_var, value=True).grid(row=6, column=0)
        tk.Radiobutton(self.window, text="Deposit", variable=self.withdraw_var, value=False).grid(row=6, column=1)

        tk.Label(self.window, text="Amount:").grid(row=7, column=0)
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=7, column=1)

        tk.Button(self.window, text="Enter", command=self.handle_transaction).grid(row=8, column=0, pady=5)
        tk.Button(self.window, text="Exit", command=self.window.quit).grid(row=8, column=1, pady=5)
        #FIX ME NEED TO SHOW THE ACTUAL BALANCE IN REAL TIME
        tk.Label(self.window, text=f"Your account balance is: ${self.account.get_balance():.2f}").grid(row=9, column=0, columnspan=2)

    def handle_transaction(self):
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
                messagebox.showinfo("Success", f"{action} successful! New balance: ${self.account.get_balance():.2f}")
            else:
                messagebox.showerror("Error", f"{action} failed. Check balance or amount.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def save_account(self, name, pin, balance):
        file_exists = os.path.isfile("ATM.csv")
        with open("ATM.csv", mode="a", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                writer.writerow(["Name", "Pin", "Balance"])
            writer.writerow([name, pin, f'${balance:.2f}'])

    def load_account(self, name, pin):
        try:
            with open("ATM.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[0] == name and row[1] == pin:
                        self.account = Account(name, float(row[2]))
                        return True
            return False
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    AccountGUI()
