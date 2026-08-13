import mariadb
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD="),
        database=os.getenv("Hostel_Management"),
    )


# def get_connection():
#   return mariadb.connect(
#      host="localhost",
#      port=3306,
#      user="root",
#        password=" ",
#       database="hostel_management")
