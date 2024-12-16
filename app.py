import streamlit as st
import mysql.connector
from mysql.connector import errorcode
import random

# MySQL Database configuration
config = {
    'user': 'root',
    'password': 'Shashwat@5',
    'host': '127.0.0.1',
    'database': 'Bank',
    'raise_on_warnings': True
}


# Database Functions
def get_db_connection():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        return db, cursor
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return None, None


def close_db_connection(db, cursor):
    if db:
        cursor.close()
        db.close()


def create_account(holder_name, holder_age, pan_no, mobile_no, initial_balance=0.0):
    db, cursor = get_db_connection()
    if not db:
        return "Database connection failed!"

    try:
        while True:
            account_number = random.randint(100000, 999999)
            cursor.execute("SELECT account_number FROM accounts WHERE account_number = %s", (account_number,))
            if cursor.fetchone() is None:
                break
        
        cursor.execute(
            "INSERT INTO accounts (account_number, holder_name, holder_age, pan_no, mobile_no, balance) VALUES (%s, %s, %s, %s, %s, %s)",
            (account_number, holder_name, holder_age, pan_no, mobile_no, initial_balance)
        )
        db.commit()
        return f"Account {account_number} created successfully for {holder_name} with initial balance ${initial_balance:.2f}"
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        close_db_connection(db, cursor)


def deposit(account_number, amount):
    db, cursor = get_db_connection()
    if not db:
        return "Database connection failed!"

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()
        if account is None:
            return f"Account {account_number} does not exist."

        new_balance = account[0] + amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        cursor.execute(
            "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
            (account_number, 'deposit', amount)
        )
        db.commit()
        return f"Successfully deposited ${amount:.2f}. New balance: ${new_balance:.2f}"
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        close_db_connection(db, cursor)


def withdraw(account_number, amount):
    db, cursor = get_db_connection()
    if not db:
        return "Database connection failed!"

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()
        if account is None:
            return f"Account {account_number} does not exist."

        current_balance = account[0]
        if amount > current_balance:
            return f"Insufficient funds! Current balance is ${current_balance:.2f}."

        new_balance = current_balance - amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        cursor.execute(
            "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
            (account_number, 'withdraw', amount)
        )
        db.commit()
        return f"Successfully withdrew ${amount:.2f}. New balance: ${new_balance:.2f}"
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        close_db_connection(db, cursor)


def enquire_balance(account_number):
    db, cursor = get_db_connection()
    if not db:
        return "Database connection failed!"
        
    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()
        if account:
            return f"Account {account_number} balance: ${account[0]:.2f}"
        return f"Account {account_number} does not exist."
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        close_db_connection(db, cursor)


def transfer(from_account, to_account, amount):
    db, cursor = get_db_connection()
    if not db:
        return "Database connection failed!"
        
    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (from_account,))
        from_account_data = cursor.fetchone()
        
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (to_account,))
        to_account_data = cursor.fetchone()

        if not from_account_data:
            return f"Source account {from_account} does not exist."
        if not to_account_data:
            return f"Destination account {to_account} does not exist."

        from_balance = from_account_data[0]
        if amount > from_balance:
            return f"Insufficient funds in account {from_account}. Current balance: ${from_balance:.2f}"

        new_from_balance = from_balance - amount
        new_to_balance = to_account_data[0] + amount

        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_from_balance, from_account))
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_to_balance, to_account))

        cursor.execute(
            "INSERT INTO transactions (account_number, transaction_type, amount, related_account) VALUES (%s, %s, %s, %s)",
            (from_account, 'transfer', amount, to_account)
        )
        cursor.execute(
            "INSERT INTO transactions (account_number, transaction_type, amount, related_account) VALUES (%s, %s, %s, %s)",
            (to_account, 'transfer', amount, from_account)
        )
        db.commit()
        return f"Successfully transferred ${amount:.2f} from {from_account} to {to_account}."
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        close_db_connection(db, cursor)


# Streamlit Application
def main():
    st.title("Bank Management System")

    menu = ["Create Account", "Deposit Money", "Withdraw Money", "Balance Inquiry", "Transfer Money", "Mini Statement", "Delete Account"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Create Account":
        st.subheader("Create a New Account")
        holder_name = st.text_input("Account Holder Name")
        holder_age = st.number_input("Holder Age", min_value=18, max_value=100, step=1)
        pan_no = st.text_input("PAN Number")
        mobile_no = st.text_input("Mobile Number")
        initial_balance = st.number_input("Initial Balance", min_value=0.0, step=0.01)

        if st.button("Create Account"):
            result = create_account(holder_name, holder_age, pan_no, mobile_no, initial_balance)
            st.success(result)

    elif choice == "Deposit Money":
        st.subheader("Deposit Money")
        account_number = st.text_input("Account Number")
        amount = st.number_input("Amount to Deposit", min_value=0.0, step=0.01)

        if st.button("Deposit"):
            st.success(deposit(account_number, amount))

    elif choice == "Withdraw Money":
        st.subheader("Withdraw Money")
        account_number = st.text_input("Account Number")
        amount = st.number_input("Amount to Withdraw", min_value=0.0, step=0.01)

        if st.button("Withdraw"):
            st.success(withdraw(account_number, amount))

    elif choice == "Balance Inquiry":
        st.subheader("Balance Inquiry")
        account_number = st.text_input("Account Number")

        if st.button("Check Balance"):
            st.success(enquire_balance(account_number))

    elif choice == "Transfer Money":
        st.subheader("Transfer Money")
        from_account = st.text_input("From Account Number")
        to_account = st.text_input("To Account Number")
        amount = st.number_input("Amount to Transfer", min_value=0.0, step=0.01)

        if st.button("Transfer"):
            st.success(transfer(from_account, to_account, amount))

if __name__ == "__main__":
    main()
