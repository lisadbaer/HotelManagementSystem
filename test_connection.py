from database import get_connection

try:
    connection = get_connection()

    print("SUCCESS!")
    print("Connected to MariaDB.")

    connection.close()

except Exception as e:
    print("FAILED!")
    print(e)
