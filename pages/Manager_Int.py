import streamlit as st
from database import get_connection
from backup import create_backup

st.title("Manager Dashboard")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM Student")
students = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Room")
rooms = cursor.fetchone()[0]

cursor.execute(
    """
    SELECT COUNT(*)
    FROM Allocation
    WHERE Status = 'Active'
    """
)
allocated = cursor.fetchone()[0]

cursor.execute(
    """
    SELECT COUNT(*)
    FROM Bed
    WHERE Status = 'Vacant'
    """
)
vacant_beds = cursor.fetchone()[0]

cursor.close()
conn.close()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", students)
col2.metric("Rooms", rooms)
col3.metric("Active Allocations", allocated)
col4.metric("Vacant Beds", vacant_beds)

st.divider()

st.subheader("Database Management")

if st.button("Backup Database"):
    try:
        filename = create_backup()
        st.success(f"Backup created successfully: {filename}")
    except Exception as e:
        st.error(f"Backup failed: {e}")


if st.button("Logout"):
    st.session_state.clear()
    st.rerun()