import mariadb
from database import get_connection


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT UserID, Role
        FROM UserAccount
        WHERE Username = ?
        AND PasswordHash = ?
    """,
        (username, password),
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
