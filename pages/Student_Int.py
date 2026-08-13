import streamlit as st
import pandas as pd
from database import get_connection
from datetime import date


# -----------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------
st.set_page_config(
    page_title="Student Dashboard",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------------------------------
# SIMPLE STYLING
# -----------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f7f7;
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e5e7eb;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------------------
# ACCESS CONTROL
# -----------------------------------------------------
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


student_id = st.session_state.user_id


# -----------------------------------------------------
# TITLE
# -----------------------------------------------------
st.title("🎓 Student Dashboard")

st.caption(
    "View your allocation, payments, maintenance requests and visits."
)


# -----------------------------------------------------
# SIDEBAR MENU
# -----------------------------------------------------
if "student_menu" not in st.session_state:
    st.session_state.student_menu = "My Allocation"


st.sidebar.header("Student Menu")


if st.sidebar.button(
    "My Allocation",
    use_container_width=True
):
    st.session_state.student_menu = "My Allocation"


if st.sidebar.button(
    "Make Payment",
    use_container_width=True
):
    st.session_state.student_menu = "Make Payment"


if st.sidebar.button(
    "Payment History",
    use_container_width=True
):
    st.session_state.student_menu = "My Payments"


if st.sidebar.button(
    "Maintenance Request",
    use_container_width=True
):
    st.session_state.student_menu = "Send Maintenance Request"


if st.sidebar.button(
    "Maintenance History",
    use_container_width=True
):
    st.session_state.student_menu = "My Maintenance"


if st.sidebar.button(
    "My Visits",
    use_container_width=True
):
    st.session_state.student_menu = "My Visits"


menu = st.session_state.student_menu


# =====================================================
# MY ALLOCATION
# =====================================================
if menu == "My Allocation":

    st.header("My Allocation")

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

        (
            first_name,
            last_name,
            number,
            hostel,
            room,
            bed,
            start_date,
            end_date
        ) = student


        st.subheader(
            f"Welcome, {first_name} {last_name}"
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Hostel",
            hostel
        )

        col2.metric(
            "Room",
            room
        )

        col3.metric(
            "Bed",
            bed
        )


        st.write("**Student ID:**", number)
        st.write("**Allocation Start:**", start_date)
        st.write("**Allocation End:**", end_date)


    else:

        st.warning(
            "You do not currently have an active allocation."
        )


# =====================================================
# MAKE PAYMENT
# =====================================================
elif menu == "Make Payment":

    st.header("Make Payment")

    st.caption(
        "Record a payment for your current hostel allocation."
    )


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT AllocationID
        FROM Allocation
        WHERE StudentID = ?
          AND Status = 'Active'
        """,
        (student_id,)
    )


    allocation = cursor.fetchone()


    if not allocation:

        st.warning(
            "You need an active allocation before making a payment."
        )


    else:

        allocation_id = allocation[0]


        cursor.execute(
            """
            SELECT Balance_Due
            FROM Payment
            WHERE AllocationID = ?
            ORDER BY
                Payment_Date DESC,
                PaymentID DESC
            LIMIT 1
            """,
            (allocation_id,)
        )


        previous = cursor.fetchone()


        if previous:

            current_balance = float(
                previous[0]
            )

            st.info(
                f"Current balance: GHS {current_balance:.2f}"
            )


        else:

            current_balance = st.number_input(
                "Total Hostel Fee",
                min_value=0.01
            )


        payment_id = st.text_input(
            "Payment ID",
            placeholder="Example: P00041"
        )


        amount = st.number_input(
            "Amount Paid",
            min_value=0.01
        )


        method = st.selectbox(
            "Payment Method",
            [
                "Mobile Money",
                "Bank Transfer",
                "Cash"
            ]
        )


        deadline = st.date_input(
            "Payment Deadline"
        )


        if st.button(
            "Submit Payment",
            use_container_width=True
        ):

            if not payment_id.strip():

                st.warning(
                    "Please enter a Payment ID."
                )


            elif amount > current_balance:

                st.warning(
                    "Payment cannot be greater than the remaining balance."
                )


            else:

                balance = (
                    current_balance - amount
                )


                payment_status = (
                    "Paid"
                    if balance == 0
                    else "Pending"
                )


                try:

                    cursor.execute(
                        """
                        INSERT INTO Payment
                        (
                            PaymentID,
                            AllocationID,
                            StudentID,
                            Amount_paid,
                            Payment_Date,
                            Payment_Method,
                            Payment_Status,
                            Balance_Due,
                            Deadline
                        )

                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            payment_id,
                            allocation_id,
                            student_id,
                            amount,
                            date.today(),
                            method,
                            payment_status,
                            balance,
                            deadline
                        )
                    )


                    conn.commit()


                    st.success(
                        f"Payment recorded successfully. "
                        f"Remaining balance: GHS {balance:.2f}"
                    )


                except Exception as e:

                    conn.rollback()

                    st.error(
                        f"Could not record payment: {e}"
                    )


    cursor.close()
    conn.close()


# =====================================================
# PAYMENT HISTORY
# =====================================================
elif menu == "My Payments":

    st.header("Payment History")


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

        ORDER BY
            Payment_Date DESC
        """,
        (student_id,)
    )


    payments = cursor.fetchall()


    cursor.close()
    conn.close()


    if payments:

        df = pd.DataFrame(
            payments,
            columns=[
                "Payment ID",
                "Amount Paid",
                "Payment Date",
                "Payment Method",
                "Status",
                "Balance Due",
                "Deadline"
            ]
        )


        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No payment records found."
        )


# =====================================================
# SEND MAINTENANCE REQUEST
# =====================================================
elif menu == "Send Maintenance Request":

    st.header("Maintenance Request")

    st.caption(
        "Report a maintenance issue in your allocated room."
    )


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            r.RoomID,
            r.RoomNumber

        FROM Allocation a

        JOIN Bed bed
            ON a.BedID = bed.BedID

        JOIN Room r
            ON bed.RoomID = r.RoomID

        WHERE a.StudentID = ?
          AND a.Status = 'Active'
        """,
        (student_id,)
    )


    room = cursor.fetchone()


    if not room:

        st.warning(
            "You need an active allocation before submitting a maintenance request."
        )


    else:

        room_id, room_number = room


        st.info(
            f"Room: {room_number}"
        )


        issue = st.text_area(
            "Describe the maintenance problem"
        )


        if st.button(
            "Submit Request",
            use_container_width=True
        ):

            if not issue.strip():

                st.warning(
                    "Please describe the maintenance issue."
                )


            else:

                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            MAX(
                                CAST(
                                    SUBSTRING(
                                        MaintenanceID,
                                        2
                                    )
                                    AS UNSIGNED
                                )
                            ),
                            0
                        ) + 1

                    FROM Maintenance
                    """
                )


                number = cursor.fetchone()[0]

                maintenance_id = (
                    f"M{number}"
                )


                cursor.execute(
                    """
                    INSERT INTO Maintenance
                    (
                        MaintenanceID,
                        RoomID,
                        StudentID,
                        IssueDescription,
                        RequestDate,
                        Status
                    )

                    VALUES (?, ?, ?, ?, ?, 'Pending')
                    """,
                    (
                        maintenance_id,
                        room_id,
                        student_id,
                        issue,
                        date.today()
                    )
                )


                conn.commit()


                st.success(
                    f"Maintenance request {maintenance_id} submitted."
                )


    cursor.close()
    conn.close()


# =====================================================
# MAINTENANCE HISTORY
# =====================================================
elif menu == "My Maintenance":

    st.header("Maintenance History")


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

        ORDER BY
            RequestDate DESC
        """,
        (student_id,)
    )


    requests = cursor.fetchall()


    cursor.close()
    conn.close()


    if requests:

        df = pd.DataFrame(
            requests,
            columns=[
                "Maintenance ID",
                "Room ID",
                "Issue",
                "Request Date",
                "Status",
                "Date Resolved"
            ]
        )


        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No maintenance requests found."
        )


# =====================================================
# MY VISITS
# =====================================================
elif menu == "My Visits":

    st.header("My Visits")


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            v.VisitID,
            vr.VisitorName,
            vr.Phone,
            v.VisitDate,
            v.CheckInTime,
            v.CheckOutTime

        FROM Visit v

        JOIN Visitor vr
            ON v.VisitorID =
               vr.VisitorID

        WHERE v.StudentID = ?

        ORDER BY
            v.VisitDate DESC
        """,
        (student_id,)
    )


    visits = cursor.fetchall()


    cursor.close()
    conn.close()


    if visits:

        df = pd.DataFrame(
            visits,
            columns=[
                "Visit ID",
                "Visitor Name",
                "Phone",
                "Visit Date",
                "Check-In",
                "Check-Out"
            ]
        )


        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "You do not have any recorded visits."
        )


# -----------------------------------------------------
# LOGOUT
# -----------------------------------------------------
st.sidebar.divider()


if st.sidebar.button(
    "Logout",
    use_container_width=True
):

    st.session_state.clear()

    st.switch_page("app.py")