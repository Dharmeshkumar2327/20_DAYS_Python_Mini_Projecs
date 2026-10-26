"""
ATM Simulator
-------------
A console-based ATM simulator written in pure Python.

Features
  - PIN login with 3 attempts (card gets blocked after that)
  - Check balance
  - Deposit and withdraw cash (multiples of 100, daily withdrawal limit)
  - Fast cash options
  - Mini statement (last 5 transactions)
  - Change PIN
  - Data saved to a JSON file so the balance persists between runs

Concepts used: variables, input/output, if/elif/else, while & for loops,
functions, lists, dictionaries, file handling (JSON), and exception handling.

Author: Dharmesh Kumar
"""

import json
import os
from datetime import datetime

DATA_FILE = "account_data.json"
MAX_PIN_ATTEMPTS = 3
DAILY_WITHDRAW_LIMIT = 20000
MIN_BALANCE = 0
NOTE_DENOMINATION = 100
FAST_CASH_OPTIONS = [500, 1000, 2000, 5000]

DEFAULT_ACCOUNT = {
    "name": "Demo User",
    "account_number": "XXXX-XXXX-4521",
    "pin": "1234",
    "balance": 10000.0,
    "withdrawn_today": 0.0,
    "last_withdraw_date": "",
    "transactions": [],
}


# ---------------------------------------------------------------- data ---

def load_account():
    """Load the account from the JSON file, or create a default one."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: data file was unreadable. Starting fresh.")
    return dict(DEFAULT_ACCOUNT, transactions=[])


def save_account(account):
    """Save the account to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(account, f, indent=4)


def add_transaction(account, kind, amount):
    """Record a transaction with a timestamp."""
    account["transactions"].append({
        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "type": kind,
        "amount": amount,
        "balance": account["balance"],
    })


def reset_daily_limit_if_new_day(account):
    today = datetime.now().strftime("%d-%m-%Y")
    if account.get("last_withdraw_date") != today:
        account["withdrawn_today"] = 0.0
        account["last_withdraw_date"] = today


# --------------------------------------------------------------- input ---

def get_amount(prompt):
    """Ask for a positive amount. Returns None if the input is invalid."""
    try:
        amount = float(input(prompt))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None
    if amount <= 0:
        print("Amount must be greater than zero.")
        return None
    return amount


def line():
    print("-" * 40)


# ---------------------------------------------------------- operations ---

def login(account):
    """Give the user MAX_PIN_ATTEMPTS chances to enter the right PIN."""
    attempts = 0
    while attempts < MAX_PIN_ATTEMPTS:
        pin = input("Enter your 4-digit PIN: ").strip()
        if pin == account["pin"]:
            print(f"\nWelcome, {account['name']}!")
            return True
        attempts += 1
        left = MAX_PIN_ATTEMPTS - attempts
        if left > 0:
            print(f"Wrong PIN. {left} attempt(s) left.")
    print("Too many wrong attempts. Your card has been blocked.")
    return False


def check_balance(account):
    line()
    print(f"Account : {account['account_number']}")
    print(f"Balance : Rs. {account['balance']:,.2f}")
    line()


def deposit(account):
    amount = get_amount("Enter amount to deposit: Rs. ")
    if amount is None:
        return
    if amount % NOTE_DENOMINATION != 0:
        print(f"Please deposit in multiples of {NOTE_DENOMINATION}.")
        return
    account["balance"] += amount
    add_transaction(account, "Deposit", amount)
    save_account(account)
    print(f"Rs. {amount:,.2f} deposited successfully.")
    print(f"New balance: Rs. {account['balance']:,.2f}")


def process_withdrawal(account, amount):
    """Shared checks for normal withdraw and fast cash."""
    reset_daily_limit_if_new_day(account)

    if amount % NOTE_DENOMINATION != 0:
        print(f"Amount must be a multiple of {NOTE_DENOMINATION}.")
    elif amount > account["balance"] - MIN_BALANCE:
        print("Insufficient balance.")
    elif account["withdrawn_today"] + amount > DAILY_WITHDRAW_LIMIT:
        left = DAILY_WITHDRAW_LIMIT - account["withdrawn_today"]
        print(f"Daily limit exceeded. You can withdraw up to Rs. {left:,.2f} today.")
    else:
        account["balance"] -= amount
        account["withdrawn_today"] += amount
        add_transaction(account, "Withdraw", amount)
        save_account(account)
        print("Please collect your cash.")
        print(f"Remaining balance: Rs. {account['balance']:,.2f}")


def withdraw(account):
    amount = get_amount("Enter amount to withdraw: Rs. ")
    if amount is not None:
        process_withdrawal(account, amount)


def fast_cash(account):
    print("\nFast Cash")
    for i, value in enumerate(FAST_CASH_OPTIONS, start=1):
        print(f"  {i}. Rs. {value:,}")
    choice = input("Choose an option: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(FAST_CASH_OPTIONS):
        process_withdrawal(account, FAST_CASH_OPTIONS[int(choice) - 1])
    else:
        print("Invalid option.")


def mini_statement(account, count=5):
    line()
    print("MINI STATEMENT (last 5 transactions)")
    line()
    recent = account["transactions"][-count:]
    if not recent:
        print("No transactions yet.")
    for t in recent:
        print(f"{t['time']}  {t['type']:<9} Rs. {t['amount']:>10,.2f}")
    line()
    print(f"Available balance: Rs. {account['balance']:,.2f}")
    line()


def change_pin(account):
    old = input("Enter current PIN: ").strip()
    if old != account["pin"]:
        print("Incorrect PIN.")
        return
    new = input("Enter new 4-digit PIN: ").strip()
    if not (new.isdigit() and len(new) == 4):
        print("PIN must be exactly 4 digits.")
        return
    if new == old:
        print("New PIN must be different from the old PIN.")
        return
    confirm = input("Confirm new PIN: ").strip()
    if new != confirm:
        print("PINs do not match.")
        return
    account["pin"] = new
    save_account(account)
    print("PIN changed successfully.")


# ---------------------------------------------------------------- main ---

MENU = """
=========== ATM MENU ===========
 1. Check Balance
 2. Deposit
 3. Withdraw
 4. Fast Cash
 5. Mini Statement
 6. Change PIN
 7. Exit
================================"""

ACTIONS = {
    "1": check_balance,
    "2": deposit,
    "3": withdraw,
    "4": fast_cash,
    "5": mini_statement,
    "6": change_pin,
}


def main():
    print("=" * 40)
    print("      WELCOME TO PYTHON ATM")
    print("=" * 40)

    account = load_account()
    if not login(account):
        return

    while True:
        print(MENU)
        choice = input("Select an option (1-7): ").strip()
        if choice == "7":
            print("Thank you for banking with us. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action(account)
        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSession ended. Goodbye!")
