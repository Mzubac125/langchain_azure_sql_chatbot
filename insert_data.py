import random
from datetime import datetime, timedelta
import pyodbc
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Sample data pools
branches = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Ottawa']
portfolio_managers = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan']
names = ['John Smith', 'Jane Doe', 'Emily Davis', 'Michael Brown', 'Laura Wilson', 'Kevin Johnson']

# Generate random date within the last year
def random_date():
    start_date = datetime.now() - timedelta(days=365)
    return (start_date + timedelta(days=random.randint(0, 365))).date()

# Connect to Azure SQL
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
    f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
    f"UID={os.getenv('AZURE_SQL_USERNAME')};"
    f"PWD={os.getenv('AZURE_SQL_PASSWORD')};"
    "Encrypt=yes;TrustServerCertificate=yes"
)

cursor = conn.cursor()

# Insert 500 rows
for i in range(1, 501):
    membernbr = random.randint(100000, 999999)
    membername = random.choice(names)
    date_added = random_date()
    portfolio_manager = random.choice(portfolio_managers)
    branch = random.choice(branches)
    profit = round(random.uniform(-5000, 20000), 2)

    cursor.execute("""
        INSERT INTO Members (membernbr, membername, date_added, portfolio_manager, branch, profit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, membernbr, membername, date_added, portfolio_manager, branch, profit)

conn.commit()
conn.close()

print("Inserted 500 rows into Members table.")
