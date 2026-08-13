import hashlib
from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT UserID, Role
        FROM UserAccount
        WHERE Username = ?
        AND PasswordHash = ?
    """,
        (username, password_hash),
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
