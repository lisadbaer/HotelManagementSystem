import streamlit as st
from database import get_connection

st.title("Student Dashboard")

if "user_id" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

student_id = st.session_state.user_id

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
    (student_id,)
)

student = cursor.fetchone()

cursor.close()
conn.close()

if student:
    first_name, last_name, number, hostel, room, bed, start_date, end_date = student

    st.header(f"Welcome, {first_name} {last_name}")

    st.write("Student ID:", number)
    st.write("Hostel:", hostel)
    st.write("Room:", room)
    st.write("Bed:", bed)
    st.write("Allocation Start:", start_date)
    st.write("Allocation End:", end_date)

else:
    st.warning("You do not currently have an active room allocation.")

if st.button("Logout"):
    st.session_state.clear()
    st.rerun()