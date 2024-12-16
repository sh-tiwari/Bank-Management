# Bank Management System

DEPLOYED LINK : https://bank-management-ms4cmxrb79razkkseyyabm.streamlit.app/

## Overview

The **Bank Management System** is a simple, interactive web application built using **Streamlit** and connected to a **MySQL** database. It allows users to perform basic banking functions, such as creating a new bank account, depositing money, withdrawing money, transferring funds, checking balance, viewing mini statements, and deleting accounts.

This project aims to demonstrate the usage of Streamlit to develop an interactive web interface for performing various operations on a banking system, while the backend relies on MySQL to handle persistent data storage.

## Features

The Bank Management System offers the following features:
- **Create Account**: Users can create a new bank account with an initial deposit.
- **Deposit Money**: Users can deposit money into their accounts.
- **Withdraw Money**: Users can withdraw money from their accounts.
- **Balance Inquiry**: Users can inquire about the balance in their accounts.
- **Transfer Money**: Users can transfer money from one account to another.
- **Mini Statement**: Users can view the last 10 transactions in their account.
- **Delete Account**: Users can delete an existing bank account.

## Technologies Used

- **Streamlit**: A framework for building interactive web applications.
- **MySQL**: A relational database for storing bank account and transaction data.
- **Python**: The core programming language.
- **Random**: Used for generating random account numbers.
- **mysql-connector-python**: Python library to connect to and interact with MySQL.

## Database Schema

The system requires a MySQL database named `Bank` with the following schema:

### `accounts` Table

| Column         | Type           | Description                                            |
|----------------|----------------|--------------------------------------------------------|
| account_number | INT            | Unique identifier for each bank account                |
| holder_name    | VARCHAR(100)    | Name of the account holder                             |
| holder_age     | INT            | Age of the account holder                              |
| pan_no         | VARCHAR(12)    | Permanent Account Number of the account holder         |
| mobile_no      | VARCHAR(15)    | Mobile number of the account holder                    |
| balance        | DECIMAL(10, 2) | Current balance in the account                         |

### `transactions` Table

| Column          | Type           | Description                                          |
|-----------------|----------------|------------------------------------------------------|
| transaction_id  | INT            | Unique identifier for each transaction               |
| account_number  | INT            | The account number the transaction belongs to        |
| transaction_type| ENUM           | Type of the transaction ('deposit', 'withdraw', 'transfer') |
| amount          | DECIMAL(10, 2) | Amount of the transaction                            |
| date_time       | DATETIME       | Date and time the transaction occurred               |
| related_account | INT            | If the transaction is a transfer, this references the other account involved |

## Setup and Installation

### Prerequisites

- **Python 3.7+**
- **MySQL** (Make sure MySQL is installed and running on your local machine or remote server)


