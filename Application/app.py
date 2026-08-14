import streamlit as st
from database import get_connection


st.set_page_config(
    page_title="Hostel Management System",
    layout="centered"
)


st.markdown(
    """
    <style>

    .stApp {
        background-color: #eceff1;
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1rem;
    }

    [data-testid="stTextInput"] input {
        border-radius: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT StudentID
        FROM Student
        WHERE StudentID = ?
        """,
        (username,)
    )

    student = cursor.fetchone()

    if student and password == "student123":
        cursor.close()
        conn.close()

        return student[0], "student"


    cursor.execute(
        """
        SELECT ManagerID
        FROM Manager
        WHERE ManagerID = ?
        """,
        (username,)
    )

    manager = cursor.fetchone()

    if manager and password == "manager123":
        cursor.close()
        conn.close()

        return manager[0], "manager"


    cursor.close()
    conn.close()

    return None


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.logged_in:

    st.title("University Hostel Management System")

    st.write(
        "Manage hostel allocations, maintenance, visitors and payments."
    )

    st.divider()

    st.subheader("Login")

    username = st.text_input(
        "Username",
        placeholder="Enter Student ID or Manager ID"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not username or not password:

            st.warning(
                "Please enter your username and password."
            )

        else:

            try:

                user = login(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.role = user[1]

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

            except Exception as e:

                st.error(
                    f"Database error: {e}"
                )


else:

    if st.session_state.role == "student":

        st.switch_page(
            "pages/Student_Int.py"
        )

    elif st.session_state.role == "manager":

        st.switch_page(
            "pages/Manager_Int.py"
        )