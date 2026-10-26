# 🏧 ATM Simulator (Python)

A console-based ATM simulator built with pure Python, using no external libraries.
It mimics a real ATM: PIN login, balance check, deposits, withdrawals, fast cash, mini statement, and PIN change. Account data is saved to a JSON file, so the balance persists between runs.

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 PIN Login | 3 attempts, then the card is blocked |
| 💰 Check Balance | Shows the masked account number and the current balance |
| ➕ Deposit | Multiples of Rs. 100 only |
| ➖ Withdraw | Checks for insufficient balance and the daily limit (Rs. 20,000) |
| ⚡ Fast Cash | One-tap Rs. 500 / 1,000 / 2,000 / 5,000 |
| 🧾 Mini Statement | Last 5 transactions with date and time |
| 🔄 Change PIN | Verifies the old PIN, requires 4 digits, confirms the new PIN |
| 💾 Persistence | Data is stored in `account_data.json` |

## 🚀 Getting Started

**Requirements:** Python 3.7 or newer (no packages to install)

```bash
git clone https://github.com/<your-username>/atm-simulator.git
cd atm-simulator
python atm_simulator.py
```

**Default PIN:** `1234`  
**Starting balance:** Rs. 10,000

To reset the account, delete `account_data.json`.

## 🖥️ Sample Output

```
========================================
      WELCOME TO PYTHON ATM
========================================
Enter your 4-digit PIN: 1234

Welcome, Demo User!

=========== ATM MENU ===========
 1. Check Balance
 2. Deposit
 3. Withdraw
 4. Fast Cash
 5. Mini Statement
 6. Change PIN
 7. Exit
================================
Select an option (1-7): 3
Enter amount to withdraw: Rs. 2500
Please collect your cash.
Remaining balance: Rs. 7,500.00
```

## 📚 Python Concepts Used

- Variables, input/output, and string formatting
- `if / elif / else` decisions
- `while` and `for` loops
- Functions, plus a dictionary of functions for the menu
- Lists and dictionaries
- File handling with `json`
- Exception handling (`try / except`)
- `datetime` for timestamps

## 🔮 Future Enhancements

- Support for multiple user accounts
- PIN hashing for security
- Transfer funds between accounts
- GUI version using Tkinter
- Unit tests with `unittest`

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
Made with ❤️ by **Dharmesh Kumar**
