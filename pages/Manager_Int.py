import streamlit as st
from database import get_connection
import os

st.title("Manager Dashboard")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM students")
students = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM rooms")
rooms = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM allocations")
allocated = cursor.fetchone()[0]

cursor.close()
conn.close()

col1, col2, col3 = st.columns(3)

col1.metric("Students", students)
col2.metric("Rooms", rooms)
col3.metric("Allocated Beds", allocated)

st.divider()

st.subheader("Database Management")

st.button("Backup Database")
st.button("Restore Database")
