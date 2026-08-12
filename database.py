import mariadb


def get_connection():
    return mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password=" ",
        database="hostel_management",
    )
