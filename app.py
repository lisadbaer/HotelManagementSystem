import streamlit as st
import mariadb

from database import get_connection


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, role
        FROM users
        WHERE username = ? AND password = ?
    """,
        (username, password),
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


st.title("Hostel Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.role = user[1]

            st.rerun()

        else:
            st.error("Invalid username or password")


else:
    st.success("Login successful")

    if st.session_state.role == "student":
        st.switch_page("pages/student.py")

    elif st.session_state.role == "manager":
        st.switch_page("pages/manager.py")
