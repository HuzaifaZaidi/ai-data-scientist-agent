import psycopg


# PostgreSQL connection details
connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ecommerce_db",
    user="postgres",
    password="Mynewpassword"
)


print("Connected to PostgreSQL successfully!")


# Close the connection
connection.close()

print("Connection closed.")