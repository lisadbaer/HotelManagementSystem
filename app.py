import streamlit as st
from database import get_connection


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    # Student login
    cursor.execute(
        """
        SELECT StudentID
        FROM Student
        WHERE StudentID = ?
        """,
        (username,),
    )

    student = cursor.fetchone()

    if student and password == "student123":
        cursor.close()
        conn.close()

        return student[0], "student"

    # Manager login
    cursor.execute(
        """
        SELECT ManagerID
        FROM Manager
        WHERE ManagerID = ?
        """,
        (username,),
    )

    manager = cursor.fetchone()

    if manager and password == "manager123":
        cursor.close()
        conn.close()

        return manager[0], "manager"

    cursor.close()
    conn.close()

    return None


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
    if st.session_state.role == "student":
        st.switch_page("pages/Student_Int.py")

    elif st.session_state.role == "manager":
        st.switch_page("pages/Manager_Int.py")
