import streamlit as st
from database import get_connection


# -----------------------------
# ACCESS CONTROL
# -----------------------------
if (
    "logged_in" not in st.session_state
    or "role" not in st.session_state
    or "user_id" not in st.session_state
):
    st.warning("Please log in first.")
    st.stop()

if st.session_state.role != "student":
    st.error("Student access only.")
    st.stop()


# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("Student Dashboard")

student_id = st.session_state.user_id


# -----------------------------
# MENU
# -----------------------------
menu = st.sidebar.selectbox("Menu", ["My Allocation", "My Payments", "My Maintenance"])


# -----------------------------
# MY ALLOCATION
# -----------------------------
if menu == "My Allocation":
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            s.FirstName,
            s.LastName,
            s.StudentID,
            h.HostelName,
            r.RoomNumber,
            bed.BedLabel,
            a.AllocationStartDate,
            a.AllocationEndDate
        FROM Student s
        JOIN Allocation a
            ON s.StudentID = a.StudentID
        JOIN Bed bed
            ON a.BedID = bed.BedID
        JOIN Room r
            ON bed.RoomID = r.RoomID
        JOIN Block b
            ON r.BlockID = b.BlockID
        JOIN Hostel h
            ON b.HostelID = h.HostelID
        WHERE s.StudentID = ?
          AND a.Status = 'Active'
        """,
        (student_id,),
    )

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student:
        (first_name, last_name, number, hostel, room, bed, start_date, end_date) = (
            student
        )

        st.header(f"Welcome, {first_name} {last_name}")

        st.header(f"Welcome, {first_name} {last_name}")

        st.write("Student ID:", number)
        st.write("Hostel:", hostel)
        st.write("Room:", room)
        st.write("Bed:", bed)
        st.write("Allocation Start:", start_date)
        st.write("Allocation End:", end_date)

    else:
        st.warning("You do not currently have an active room allocation.")


# -----------------------------
# MY PAYMENTS
# -----------------------------
elif menu == "My Payments":
    st.subheader("Payment History")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            PaymentID,
            Amount_paid,
            Payment_Date,
            Payment_Method,
            Payment_Status,
            Balance_Due,
            Deadline
        FROM Payment
        WHERE StudentID = ?
        ORDER BY Payment_Date DESC
        """,
        (student_id,),
    )

    payments = cursor.fetchall()

    cursor.close()
    conn.close()

    if payments:
        st.dataframe(payments, use_container_width=True)
    else:
        st.info("No payment records found.")


# -----------------------------
# MY MAINTENANCE
# -----------------------------
elif menu == "My Maintenance":
    st.subheader("Maintenance Requests")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            MaintenanceID,
            RoomID,
            IssueDescription,
            RequestDate,
            Status,
            DateResolved
        FROM Maintenance
        WHERE StudentID = ?
        ORDER BY RequestDate DESC
        """,
        (student_id,),
    )

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    if requests:
        st.dataframe(requests, use_container_width=True)
    else:
        st.info("No maintenance requests found.")


# -----------------------------
# LOGOUT
# -----------------------------
st.sidebar.divider()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")
