import streamlit as st
from database import get_connection
from datetime import date


# ACCESS CONTROL
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

st.title("Student Dashboard")


menu = st.sidebar.selectbox(
    "Menu",
    [
        "My Allocation",
        "Make Payment",
        "My Payments",
        "Send Maintenance Request",
        "My Maintenance",
        "My Visits"
    ]
)


# =====================================================
# MY ALLOCATION
# =====================================================

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

        st.header(
            f"Welcome, {first_name} {last_name}"
        )

        st.write("Student ID:", number)
        st.write("Hostel:", hostel)
        st.write("Room:", room)
        st.write("Bed:", bed)
        st.write("Allocation Start:", start_date)
        st.write("Allocation End:", end_date)

    else:

        st.warning(
            "You do not currently have an active allocation."
        )


# =====================================================
# MAKE PAYMENT
# =====================================================

elif menu == "Make Payment":

    st.subheader("Make Payment")

    conn = get_connection()
    cursor = conn.cursor()

    # Get active allocation
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

        # Get previous balance
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

            st.write(
                "Current Balance:",
                current_balance
            )

        else:

            current_balance = st.number_input(
                "Total Hostel Fee",
                min_value=0.01
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


        if st.button("Submit Payment"):

            if amount > current_balance:

                st.warning(
                    "Payment cannot be greater than the remaining balance."
                )

            else:

                balance = (
                    current_balance - amount
                )

                if balance == 0:
                    payment_status = "Paid"
                else:
                    payment_status = "Pending"


                cursor.execute(
                    """
                    SELECT
                        COALESCE(
                            MAX(
                                CAST(
                                    SUBSTRING(
                                        PaymentID,
                                        2
                                    ) AS UNSIGNED
                                )
                            ),
                            0
                        ) + 1
                    FROM Payment
                    """
                )

                next_number = (
                    cursor.fetchone()[0]
                )

                payment_id = (
                    f"P{next_number:05d}"
                )


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
                    f"Payment recorded. Remaining balance: {balance:.2f}"
                )


    cursor.close()
    conn.close()


# =====================================================
# MY PAYMENTS
# =====================================================

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
        (student_id,)
    )

    payments = cursor.fetchall()

    cursor.close()
    conn.close()

    if payments:

        st.dataframe(
            payments,
            use_container_width=True
        )

    else:

        st.info(
            "No payment records found."
        )


# =====================================================
# SEND MAINTENANCE REQUEST
# =====================================================

elif menu == "Send Maintenance Request":

    st.subheader(
        "Send Maintenance Request"
    )

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            r.RoomID,
            r.RoomNumber
        FROM Allocation a

        JOIN Bed b
            ON a.BedID = b.BedID

        JOIN Room r
            ON b.RoomID = r.RoomID

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

        st.write(
            "Room:",
            room_number
        )

        issue = st.text_area(
            "Describe the problem"
        )


        if st.button(
            "Submit Maintenance Request"
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
                                    ) AS UNSIGNED
                                )
                            ),
                            0
                        ) + 1
                    FROM Maintenance
                    """
                )

                next_number = (
                    cursor.fetchone()[0]
                )

                maintenance_id = (
                    f"M{next_number}"
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
# MY MAINTENANCE
# =====================================================

elif menu == "My Maintenance":

    st.subheader(
        "My Maintenance Requests"
    )

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
        (student_id,)
    )

    requests = cursor.fetchall()

    cursor.close()
    conn.close()

    if requests:

        st.dataframe(
            requests,
            use_container_width=True
        )

    else:

        st.info(
            "No maintenance requests found."
        )


# =====================================================
# MY VISITS
# =====================================================

elif menu == "My Visits":

    st.subheader(
        "Visitors Who Have Visited Me"
    )

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
            ON v.VisitorID = vr.VisitorID

        WHERE v.StudentID = ?

        ORDER BY v.VisitDate DESC
        """,
        (student_id,)
    )

    visits = cursor.fetchall()

    cursor.close()
    conn.close()

    if visits:

        st.dataframe(
            visits,
            use_container_width=True
        )

    else:

        st.info(
            "You do not have any recorded visits."
        )


# =====================================================
# LOGOUT
# =====================================================

st.sidebar.divider()

if st.sidebar.button("Logout"):

    st.session_state.clear()

    st.switch_page("app.py")