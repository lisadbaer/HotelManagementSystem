import streamlit as st
from database import get_connection
from backup import create_backup

# -----------------------------
# ACCESS CONTROL
# -----------------------------
if "logged_in" not in st.session_state or st.session_state.role != "manager":
    st.error("Manager access only.")
    st.stop()

st.title("Manager Dashboard")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Manage Students", "Search Students", "Reports"]
)

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Student")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Room")
    rooms = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Allocation
        WHERE Status = 'Active'
    """)
    allocations = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Bed
        WHERE Status = 'Vacant'
    """)
    vacant_beds = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", students)
    col2.metric("Rooms", rooms)
    col3.metric("Active Allocations", allocations)
    col4.metric("Vacant Beds", vacant_beds)

    st.subheader("Database Backup")

    if st.button("Backup Database"):
        try:
            filename = create_backup()
            st.success(f"Backup created: {filename}")
        except Exception as e:
            st.error(f"Backup failed: {e}")


# -----------------------------
# STUDENT CRUD
# -----------------------------
elif menu == "Manage Students":

    st.header("Manage Students")

    action = st.selectbox(
        "Choose Action",
        ["View", "Add", "Update", "Delete"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    # READ
    if action == "View":

        cursor.execute("""
            SELECT
                StudentID,
                FirstName,
                LastName,
                Gender,
                Programme,
                Year
            FROM Student
        """)

        st.dataframe(cursor.fetchall())

    # CREATE
    elif action == "Add":

        student_id = st.text_input("Student ID")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        email = st.text_input("Email")

        programme = st.selectbox(
            "Programme",
            ["CS", "BA", "ENG", "LLB"]
        )

        year = st.number_input(
            "Year",
            min_value=2026,
            max_value=2035
        )

        if st.button("Add Student"):

            if not student_id or not first_name or not last_name:
                st.error("Please complete the required fields.")

            elif "@" not in email:
                st.error("Enter a valid email.")

            else:
                try:
                    cursor.execute("""
                        INSERT INTO Student
                        (
                            StudentID,
                            FirstName,
                            LastName,
                            Gender,
                            Email,
                            Programme,
                            Year
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        student_id,
                        first_name,
                        last_name,
                        gender,
                        email,
                        programme,
                        year
                    ))

                    conn.commit()
                    st.success("Student added successfully.")

                except Exception as e:
                    st.error(f"Could not add student: {e}")

    # UPDATE
    elif action == "Update":

        student_id = st.text_input("Student ID")
        new_email = st.text_input("New Email")
        new_phone = st.text_input("New Phone")

        if st.button("Update Student"):

            cursor.execute("""
                UPDATE Student
                SET Email = ?, Phone = ?
                WHERE StudentID = ?
            """,
            (
                new_email,
                new_phone,
                student_id
            ))

            conn.commit()

            if cursor.rowcount > 0:
                st.success("Student updated.")
            else:
                st.warning("Student not found.")

    # DELETE
    elif action == "Delete":

        student_id = st.text_input(
            "Student ID to delete"
        )

        if st.button("Delete Student"):

            try:
                cursor.execute("""
                    DELETE FROM Student
                    WHERE StudentID = ?
                """,
                (student_id,))

                conn.commit()

                if cursor.rowcount > 0:
                    st.success("Student deleted.")
                else:
                    st.warning("Student not found.")

            except Exception:
                st.error(
                    "Student cannot be deleted because related records exist."
                )

    cursor.close()
    conn.close()


# -----------------------------
# SEARCH AND FILTER
# -----------------------------
elif menu == "Search Students":

    st.header("Search Students")

    search = st.text_input(
        "Enter Student ID or Name"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            StudentID,
            FirstName,
            LastName,
            Gender,
            Programme,
            Year
        FROM Student
        WHERE StudentID LIKE ?
           OR FirstName LIKE ?
           OR LastName LIKE ?
    """,
    (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
    ))

    results = cursor.fetchall()

    st.dataframe(results)

    cursor.close()
    conn.close()


# -----------------------------
# REPORTS
# -----------------------------
elif menu == "Reports":

    st.header("Reports")

    report = st.selectbox(
        "Choose Report",
        [
            "Hostel Occupancy",
            "Outstanding Payments"
        ]
    )

    conn = get_connection()
    cursor = conn.cursor()

    if report == "Hostel Occupancy":

        cursor.execute("""
            SELECT
                h.HostelName,
                SUM(r.Capacity) AS Capacity,
                SUM(r.CurrentOccupancy) AS Occupied,
                ROUND(
                    SUM(r.CurrentOccupancy)
                    / SUM(r.Capacity) * 100,
                    2
                ) AS OccupancyRate
            FROM Hostel h
            JOIN Block b
                ON h.HostelID = b.HostelID
            JOIN Room r
                ON b.BlockID = r.BlockID
            GROUP BY h.HostelID, h.HostelName
            ORDER BY OccupancyRate DESC
        """)

    else:

        cursor.execute("""
            SELECT
                s.StudentID,
                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),
                p.Balance_Due,
                p.Deadline
            FROM Student s
            JOIN Payment p
                ON s.StudentID = p.StudentID
            WHERE p.Balance_Due > 0
        """)

    st.dataframe(cursor.fetchall())

    cursor.close()
    conn.close()


# -----------------------------
# LOGOUT
# -----------------------------
st.sidebar.divider()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("../app.py")