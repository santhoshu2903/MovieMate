import mysql.connector

# Define the connection parameters
host = "141.209.241.81"
port = 3306
user = "your_username"  # Replace with the appropriate username
password = "your_password"  # Replace with the appropriate password
database = "BIS698"

# Create a connection to the database
connection = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# Check if the connection was successful
if connection.is_connected():
    print("Connected to the database")

# Now, you can perform database operations using 'connection'

# Don't forget to close the connection when you're done
connection.close()
