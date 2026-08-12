import streamlit as st
from database import get_connection

st.title("Student Dashboard")

user_id = st.session_state.user_id

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        s.first_name,
        s.last_name,
        s.student_number,
        h.hostel_name,
        r.room_number,
        a.bed_number
    FROM students s
    JOIN allocations a
        ON s.student_id = a.student_id
    JOIN rooms r
        ON a.room_id = r.room_id
    JOIN hostels h
        ON r.hostel_id = h.hostel_id
    WHERE s.user_id = ?
""",
    (user_id,),
)

student = cursor.fetchone()

cursor.close()
conn.close()

if student:
    first_name, last_name, number, hostel, room, bed = student

    st.header(f"Welcome, {first_name} {last_name}")

    st.write("Student Number:", number)
    st.write("Hostel:", hostel)
    st.write("Room:", room)
    st.write("Bed:", bed)

else:
    st.warning("You do not currently have a room allocation.")

if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
