import mysql.connector
import random
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Shashwat@5",
        database="Bank"
    )
    cursor = db.cursor()
    print("Successfully connected to the database")  # Print success message
except mysql.connector.Error as err:
    print(f"Error: {err}")


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, holder_name,holder_age, pan_no, mobile_no, initial_balance=0.0):
        try:
            while True:
                account_number = random.randint(100000, 999999)  # 6-digit random number
                cursor.execute("SELECT account_number FROM accounts WHERE account_number = %s", (account_number,))
                if cursor.fetchone() is None:  # Ensure the number doesn't already exist
                    break

            # Insert the new account into the database
            cursor.execute(
                "INSERT INTO accounts (account_number, holder_name, holder_age, pan_no, mobile_no, balance) VALUES (%s, %s, %s, %s, %s, %s)",
                (account_number, holder_name, holder_age, pan_no, mobile_no, initial_balance),
            )
            db.commit()
            print(f"Account {account_number} created successfully for {holder_name} with initial balance ${initial_balance:.2f}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")


    def enquire_balance(self, account_number):
        try:
            # Query to fetch the balance for the account
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account is None:
                print(f"Account {account_number} does not exist.")
                return

            # If the account exists, retrieve and print the balance
            balance = account[0]
            print(f"Account {account_number} balance: ${balance:.2f}")

        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def delete_account(self, account_number):
        try:
            # Check if the account exists in the database
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account is None:
                print(f"Account {account_number} does not exist.")
                return

            # Delete the account
            cursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
            db.commit()

            print(f"Account {account_number} has been successfully deleted.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def deposit(self, account_number, amount):
        try:
            # Check if the account exists
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account is None:
                print(f"Account {account_number} does not exist.")
                return

            # Update the balance
            current_balance = account[0]
            new_balance = current_balance + amount
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            
            # Insert transaction record
            cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
                (account_number, 'deposit', amount)
            )

            db.commit()
            print(f"Successfully deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")



    def withdraw(self, account_number, amount):
        try:
            # Check if the account exists
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account is None:
                print(f"Account {account_number} does not exist.")
                return

            current_balance = account[0]

            # Check for sufficient funds
            if amount > current_balance:
                print(f"Insufficient funds! Current balance is ${current_balance:.2f}.")
                return

            # Update the balance
            new_balance = current_balance - amount
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            
            # Insert transaction record
            cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
                (account_number, 'withdraw', amount)
            )

            db.commit()
            print(f"Successfully withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")


    def transfer(self, from_account, to_account, amount):
        try:
            # Check if both accounts exist
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (from_account,))
            from_account_data = cursor.fetchone()
            
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (to_account,))
            to_account_data = cursor.fetchone()

            if from_account_data is None:
                print(f"Source account {from_account} does not exist.")
                return
            if to_account_data is None:
                print(f"Destination account {to_account} does not exist.")
                return

            # Check if the source account has enough funds
            from_balance = from_account_data[0]

            if amount > from_balance:
                print(f"Insufficient funds in account {from_account}. Current balance: ${from_balance:.2f}")
                return

            # Perform the transfer
            new_from_balance = from_balance - amount
            new_to_balance = to_account_data[0] + amount

            # Update both accounts in the database
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_from_balance, from_account))
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_to_balance, to_account))

            # Insert transaction records
            cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, related_account) VALUES (%s, %s, %s, %s)",
                (from_account, 'transfer', amount, to_account)
            )
            cursor.execute(
                "INSERT INTO transactions (account_number, transaction_type, amount, related_account) VALUES (%s, %s, %s, %s)",
                (to_account, 'transfer', amount, from_account)
            )

            db.commit()
            print(f"Successfully transferred ${amount:.2f} from account {from_account} to account {to_account}.")
            print(f"New balance: Source: ${new_from_balance:.2f}, Destination: ${new_to_balance:.2f}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")



    def list_accounts(self):
        try:
            # Fetch all account details
            cursor.execute("SELECT account_number, holder_name, holder_age, pan_no, mobile_no, balance FROM accounts")
            accounts = cursor.fetchall()

            if not accounts:
                print("No accounts found in the database.")
                return

            print(f"{'Account Number':<15} {'Holder Name':<20} {'Age':<5} {'PAN No.':<12} {'Mobile No.':<15} {'Balance':<10}")
            print("-" * 80)
            
            # Print each account's details
            for account in accounts:
                account_number, holder_name, holder_age, pan_no, mobile_no, balance = account
                print(f"{account_number:<15} {holder_name:<20} {holder_age:<5} {pan_no:<12} {mobile_no:<15} ${balance:.2f}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def mini_statement(self, account_number):
        try:
            # Query for the last 10 transactions of the given account_number
            cursor.execute("""
                SELECT transaction_type, amount, date_time, related_account
                FROM transactions
                WHERE account_number = %s
                ORDER BY date_time DESC
                LIMIT 10
            """, (account_number,))
            
            transactions = cursor.fetchall()

            if not transactions:
                print(f"No transactions found for account {account_number}.")
                return

            print(f"\nMini Statement for Account {account_number}:\n")
            print(f"{'Transaction Type':<15}{'Amount':<10}{'Related Account':<15}{'Date Time'}")
            print("-" * 50)

            # Print each transaction with modified labels
            for transaction in transactions:
                transaction_type, amount, date_time, related_account = transaction

                # Change the transaction types based on the transaction type
                if transaction_type == 'deposit':
                    transaction_type = "Credited"
                elif transaction_type == 'withdraw':
                    transaction_type = "Debited"
                elif transaction_type == 'transfer':
                    # Check if it's a debited or credited transfer based on the source and destination account
                    if related_account == account_number:  # It's the source of transfer
                        transaction_type = "Debited"
                    else:  # It's the destination account of the transfer
                        transaction_type = "Credited"

                related_account_info = related_account if related_account else "N/A"
                print(f"{transaction_type:<15}{amount:<10}{related_account_info:<15}{date_time}")

        except mysql.connector.Error as err:
            print(f"Database error: {err}")

def main():
    my_bank = Bank()

    

    # Create accounts
    #my_bank.create_account("Shashwat Tiwari",21,"CCVPT8167J","9054936664")
    #my_bank.create_account("Jane Smith", 28, "XYZAB5678C", "8765432190", 500.75)
    # Deleting an account
    my_bank.delete_account(258546 )


    

    # Deposit money
    my_bank.deposit(149357, 200)

    # Withdraw money
    my_bank.withdraw(692914, 10)

    # Transferring money between accounts
    my_bank.transfer(149357, 692914 , 200)

    print("\nListing all accounts:")
    my_bank.list_accounts()

    my_bank.enquire_balance(149357)

    my_bank.mini_statement(692914)

    


if __name__ == "__main__":
    main()
