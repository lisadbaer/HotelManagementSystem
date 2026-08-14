import streamlit as st
import pandas as pd
from database import get_connection
from backup import create_backup
from datetime import date, timedelta


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(page_title="Manager Dashboard", layout="wide")


# =====================================================
# SIMPLE STYLING
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #eceff1;
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    [data-testid="stSidebar"] {
        background-color: #e2e6e9;
        border-right: 1px solid #cbd0d4;
    }

    [data-testid="stMetric"] {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d1d5db;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }

    [data-testid="stDataFrame"] {
        background-color: #f5f5f5;
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# ACCESS CONTROL
# =====================================================

if (
    "logged_in" not in st.session_state
    or "role" not in st.session_state
    or "user_id" not in st.session_state
):
    st.warning("Please log in first.")
    st.stop()


if st.session_state.role != "manager":
    st.error("Manager access only.")
    st.stop()


manager_id = st.session_state.user_id


# =====================================================
# PAGE TITLE
# =====================================================

st.title("Manager Dashboard")

st.caption("Manage hostel allocations, inspections, maintenance, visitors and reports.")


# =====================================================
# SIDEBAR MENU
# =====================================================

if "manager_menu" not in st.session_state:
    st.session_state.manager_menu = "Dashboard"


st.sidebar.header("Manager Menu")


menu_items = [
    "Dashboard",
    "Allocations",
    "Inspections",
    "Maintenance",
    "Student Payments",
    "Visitors",
    "Vacancy",
    "Reports",
    "Advanced Queries",
]


for item in menu_items:
    if st.sidebar.button(item, use_container_width=True):
        st.session_state.manager_menu = item


menu = st.session_state.manager_menu


# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":
    st.header("Overview")

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

    allocations = cursor.fetchone()[0]

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

    col3.metric("Active Allocations", allocations)

    col4.metric("Vacant Beds", vacant_beds)

    st.divider()

    st.subheader("Database Backup")

    if st.button("Create Backup"):
        try:
            filename = create_backup()

            st.success(f"Backup created: {filename}")

        except Exception as e:
            st.error(f"Backup failed: {e}")


# =====================================================
# ALLOCATIONS
# =====================================================

elif menu == "Allocations":
    st.header("Student Allocations")

    st.caption("Assign hostel beds or remove existing allocations.")

    action = st.radio(
        "Action", ["Give Allocation", "Remove Allocation"], horizontal=True
    )

    # -------------------------------------------------
    # GIVE ALLOCATION
    # -------------------------------------------------

    if action == "Give Allocation":
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                StudentID,
                FirstName,
                LastName,
                Gender

            FROM Student

            ORDER BY StudentID
            """
        )

        students = cursor.fetchall()

        student_options = {
            f"{sid} - {first} {last}": (sid, gender)
            for sid, first, last, gender in students
        }

        student_choice = st.selectbox("Student", list(student_options.keys()))

        student_id, gender = student_options[student_choice]

        cursor.execute(
            """
            SELECT
                bed.BedID,
                h.HostelName,
                r.RoomNumber,
                bed.BedLabel

            FROM Bed bed

            JOIN Room r
                ON bed.RoomID = r.RoomID

            JOIN Block b
                ON r.BlockID = b.BlockID

            JOIN Hostel h
                ON b.HostelID = h.HostelID

            WHERE
                bed.Status = 'Vacant'

                AND h.GenderType = ?

            ORDER BY
                h.HostelName,
                r.RoomNumber
            """,
            (gender,),
        )

        bed_rows = cursor.fetchall()

        bed_options = {
            (f"{bed_id} | {hostel} | Room {room} | Bed {label}"): bed_id
            for bed_id, hostel, room, label in bed_rows
        }

        if not bed_options:
            st.warning("No suitable vacant beds available.")

        else:
            selected_bed = st.selectbox("Available Bed", list(bed_options.keys()))

            bed_id = bed_options[selected_bed]

            cursor.execute(
                """
                SELECT SemesterID
                FROM Semester
                ORDER BY StartDate
                """
            )

            semesters = [row[0] for row in cursor.fetchall()]

            semester_id = st.selectbox("Semester", semesters)

            start_date = st.date_input("Start Date")

            end_date = st.date_input(
                "End Date", value=(start_date + timedelta(days=90))
            )

            if st.button("Create Allocation"):
                try:
                    conn.autocommit = False

                    cursor.execute(
                        """
                        SELECT COUNT(*)

                        FROM Allocation

                        WHERE StudentID = ?

                          AND Status = 'Active'
                        """,
                        (student_id,),
                    )

                    existing = cursor.fetchone()[0]

                    if existing > 0:
                        st.error("Student already has an active allocation.")

                    else:
                        cursor.execute(
                            """
                            SELECT
                                COALESCE(
                                    MAX(
                                        CAST(
                                            SUBSTRING(
                                                AllocationID,
                                                2
                                            )
                                            AS UNSIGNED
                                        )
                                    ),
                                    0
                                ) + 1

                            FROM Allocation
                            """
                        )

                        number = cursor.fetchone()[0]

                        allocation_id = f"A{number:05d}"

                        today = date.today()

                        cursor.execute(
                            """
                            INSERT INTO Allocation
                            (
                                AllocationID,
                                StudentID,
                                BedID,
                                SemesterID,
                                AllocationStartDate,
                                AllocationEndDate,
                                OfferSentDate,
                                AcceptanceDeadline,
                                AcceptedDate,
                                Status
                            )

                            VALUES
                            (
                                ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, 'Active'
                            )
                            """,
                            (
                                allocation_id,
                                student_id,
                                bed_id,
                                semester_id,
                                start_date,
                                end_date,
                                today,
                                today + timedelta(days=7),
                                today,
                            ),
                        )

                        cursor.execute(
                            """
                            UPDATE Bed
                            SET Status = 'Occupied'
                            WHERE BedID = ?
                            """,
                            (bed_id,),
                        )

                        cursor.execute(
                            """
                            SELECT RoomID
                            FROM Bed
                            WHERE BedID = ?
                            """,
                            (bed_id,),
                        )

                        room_id = cursor.fetchone()[0]

                        cursor.execute(
                            """
                            UPDATE Room

                            SET CurrentOccupancy =
                            (
                                SELECT COUNT(*)

                                FROM Bed

                                WHERE RoomID = ?

                                  AND Status =
                                      'Occupied'
                            )

                            WHERE RoomID = ?
                            """,
                            (room_id, room_id),
                        )

                        conn.commit()

                        st.success(f"Allocation {allocation_id} created successfully.")

                except Exception as e:
                    conn.rollback()

                    st.error(f"Allocation failed: {e}")

        cursor.close()
        conn.close()

    # -------------------------------------------------
    # REMOVE ALLOCATION
    # -------------------------------------------------

    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                a.AllocationID,
                a.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                a.BedID

            FROM Allocation a

            JOIN Student s
                ON a.StudentID = s.StudentID

            WHERE
                a.Status = 'Active'

            ORDER BY
                a.AllocationID
            """
        )

        rows = cursor.fetchall()

        allocation_options = {
            (f"{allocation_id} | {student_id} | {name}"): (allocation_id, bed_id)
            for allocation_id, student_id, name, bed_id in rows
        }

        if not allocation_options:
            st.info("No active allocations.")

        else:
            selected = st.selectbox(
                "Active Allocation", list(allocation_options.keys())
            )

            allocation_id, bed_id = allocation_options[selected]

            if st.button("Remove Allocation"):
                try:
                    conn.autocommit = False

                    cursor.execute(
                        """
                        UPDATE Allocation

                        SET Status = 'Inactive'

                        WHERE AllocationID = ?
                        """,
                        (allocation_id,),
                    )

                    cursor.execute(
                        """
                        UPDATE Bed

                        SET Status = 'Vacant'

                        WHERE BedID = ?
                        """,
                        (bed_id,),
                    )

                    cursor.execute(
                        """
                        SELECT RoomID

                        FROM Bed

                        WHERE BedID = ?
                        """,
                        (bed_id,),
                    )

                    room_id = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        UPDATE Room

                        SET CurrentOccupancy =
                        (
                            SELECT COUNT(*)

                            FROM Bed

                            WHERE RoomID = ?

                              AND Status =
                                  'Occupied'
                        )

                        WHERE RoomID = ?
                        """,
                        (room_id, room_id),
                    )

                    conn.commit()

                    st.success("Allocation changed to Inactive.")

                except Exception as e:
                    conn.rollback()

                    st.error(f"Could not remove allocation: {e}")

        cursor.close()
        conn.close()


# =====================================================
# INSPECTIONS
# =====================================================

elif menu == "Inspections":
    st.header("Inspection Management")

    st.caption("View, add and update room inspection records.")

    action = st.selectbox(
        "Action", ["View Inspections", "Add Inspection", "Update Inspection"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    if action == "View Inspections":
        cursor.execute(
            """
            SELECT
                InspectionID,
                RoomID,
                ManagerID,
                Inspection_date,
                RoomCondition,
                Remarks

            FROM Inspection

            ORDER BY
                Inspection_date DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Inspection ID",
                "Room ID",
                "Manager ID",
                "Inspection Date",
                "Condition",
                "Remarks",
            ],
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif action == "Add Inspection":
        cursor.execute(
            """
            SELECT RoomID
            FROM Room
            ORDER BY RoomID
            """
        )

        rooms = [row[0] for row in cursor.fetchall()]

        room_id = st.selectbox("Room", rooms)

        condition = st.selectbox("Condition", ["Good", "Fair", "Poor"])

        remarks = st.text_area("Remarks")

        inspection_date = st.date_input("Inspection Date")

        if st.button("Add Inspection"):
            cursor.execute(
                """
                SELECT
                    COALESCE(
                        MAX(
                            CAST(
                                SUBSTRING(
                                    InspectionID,
                                    2
                                )
                                AS UNSIGNED
                            )
                        ),
                        0
                    ) + 1

                FROM Inspection
                """
            )

            number = cursor.fetchone()[0]

            inspection_id = f"I{number}"

            cursor.execute(
                """
                INSERT INTO Inspection
                (
                    InspectionID,
                    RoomID,
                    ManagerID,
                    Inspection_date,
                    RoomCondition,
                    Remarks
                )

                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    inspection_id,
                    room_id,
                    manager_id,
                    inspection_date,
                    condition,
                    remarks,
                ),
            )

            conn.commit()

            st.success(f"Inspection {inspection_id} added.")

    else:
        cursor.execute(
            """
            SELECT InspectionID
            FROM Inspection
            ORDER BY InspectionID
            """
        )

        inspection_ids = [row[0] for row in cursor.fetchall()]

        inspection_id = st.selectbox("Inspection", inspection_ids)

        condition = st.selectbox("New Condition", ["Good", "Fair", "Poor"])

        remarks = st.text_area("Updated Remarks")

        if st.button("Update Inspection"):
            cursor.execute(
                """
                UPDATE Inspection

                SET RoomCondition = ?,
                    Remarks = ?

                WHERE InspectionID = ?
                """,
                (condition, remarks, inspection_id),
            )

            conn.commit()

            st.success("Inspection updated successfully.")

    cursor.close()
    conn.close()


# =====================================================
# MAINTENANCE
# =====================================================

elif menu == "Maintenance":
    st.header("Maintenance Management")

    st.caption("View requests, assign maintenance staff and update request status.")

    action = st.selectbox(
        "Action", ["View Maintenance", "Add Maintenance", "Update Maintenance"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    if action == "View Maintenance":
        cursor.execute(
            """
            SELECT
                MaintenanceID,
                RoomID,
                StudentID,
                StaffID,
                ManagerID,
                IssueDescription,
                RequestDate,
                Status,
                DateResolved

            FROM Maintenance

            ORDER BY
                RequestDate DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Maintenance ID",
                "Room ID",
                "Student ID",
                "Staff ID",
                "Manager ID",
                "Issue",
                "Request Date",
                "Status",
                "Date Resolved",
            ],
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif action == "Add Maintenance":
        cursor.execute(
            """
            SELECT RoomID
            FROM Room
            ORDER BY RoomID
            """
        )

        rooms = [row[0] for row in cursor.fetchall()]

        room_id = st.selectbox("Room", rooms)

        issue = st.text_area("Issue Description")

        if st.button("Add Maintenance Record"):
            if not issue.strip():
                st.warning("Please enter an issue description.")

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

                maintenance_id = f"M{number}"

                cursor.execute(
                    """
                    INSERT INTO Maintenance
                    (
                        MaintenanceID,
                        RoomID,
                        ManagerID,
                        IssueDescription,
                        RequestDate,
                        Status
                    )

                    VALUES
                    (?, ?, ?, ?, ?, 'Pending')
                    """,
                    (maintenance_id, room_id, manager_id, issue, date.today()),
                )

                conn.commit()

                st.success(f"Maintenance record {maintenance_id} added.")

    else:
        cursor.execute(
            """
            SELECT MaintenanceID
            FROM Maintenance
            ORDER BY MaintenanceID
            """
        )

        maintenance_ids = [row[0] for row in cursor.fetchall()]

        maintenance_id = st.selectbox("Maintenance Request", maintenance_ids)

        cursor.execute(
            """
            SELECT
                a.StaffID,

                CONCAT(
                    s.First_Name,
                    ' ',
                    s.Last_Name
                )

            FROM Auxiliary_Staff a

            JOIN Staff s
                ON a.StaffID = s.StaffID

            WHERE
                a.Role = 'Maintenance'

            ORDER BY
                s.First_Name
            """
        )

        staff_rows = cursor.fetchall()

        staff_options = {
            f"{staff_id} - {name}": staff_id for staff_id, name in staff_rows
        }

        selected_staff = st.selectbox("Assign Staff", list(staff_options.keys()))

        status = st.selectbox("Status", ["Pending", "Resolved", "Ok"])

        issue = st.text_area("Issue Description")

        if st.button("Update Maintenance"):
            resolved_date = date.today() if status == "Resolved" else None

            cursor.execute(
                """
                UPDATE Maintenance

                SET StaffID = ?,
                    ManagerID = ?,
                    IssueDescription = ?,
                    Status = ?,
                    DateResolved = ?

                WHERE MaintenanceID = ?
                """,
                (
                    staff_options[selected_staff],
                    manager_id,
                    issue,
                    status,
                    resolved_date,
                    maintenance_id,
                ),
            )

            conn.commit()

            st.success("Maintenance record updated successfully.")

    cursor.close()
    conn.close()


# =====================================================
# STUDENT PAYMENTS
# =====================================================

elif menu == "Student Payments":
    st.header("Student Payments")

    st.caption("Search and view student payment records.")

    conn = get_connection()
    cursor = conn.cursor()

    search = st.text_input("Search Student ID")

    cursor.execute(
        """
        SELECT
            p.PaymentID,
            p.StudentID,

            CONCAT(
                s.FirstName,
                ' ',
                s.LastName
            ),

            p.Amount_paid,
            p.Payment_Date,
            p.Payment_Method,
            p.Payment_Status,
            p.Balance_Due,
            p.Deadline

        FROM Payment p

        JOIN Student s
            ON p.StudentID = s.StudentID

        WHERE
            p.StudentID LIKE ?

        ORDER BY
            p.Payment_Date DESC
        """,
        (f"%{search}%",),
    )

    rows = cursor.fetchall()

    df = pd.DataFrame(
        rows,
        columns=[
            "Payment ID",
            "Student ID",
            "Student Name",
            "Amount Paid",
            "Payment Date",
            "Payment Method",
            "Status",
            "Balance Due",
            "Deadline",
        ],
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    cursor.close()
    conn.close()


# =====================================================
# VISITORS
# =====================================================

elif menu == "Visitors":
    st.header("Visitor Management")

    st.caption("Manage visitor approvals and hostel visit records.")

    action = st.selectbox(
        "Action",
        [
            "View Visitors",
            "Add Visitor",
            "Approve / Reject Visitor",
            "Record Visit",
            "View Visits",
        ],
    )

    conn = get_connection()
    cursor = conn.cursor()

    if action == "View Visitors":
        cursor.execute(
            """
            SELECT
                VisitorID,
                VisitorName,
                Phone,
                ApprovalStatus

            FROM Visitor

            ORDER BY
                VisitorName
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows, columns=["Visitor ID", "Visitor Name", "Phone", "Status"]
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

    elif action == "Add Visitor":
        visitor_id = st.text_input("Visitor ID")

        name = st.text_input("Visitor Name")

        phone = st.text_input("Phone")

        approval_status = st.selectbox("Approval Status", ["Approved", "Rejected"])

        if st.button("Add Visitor"):
            if not visitor_id or not name:
                st.warning("Visitor ID and name are required.")

            else:
                try:
                    cursor.execute(
                        """
                        INSERT INTO Visitor
                        (
                            VisitorID,
                            VisitorName,
                            Phone,
                            ApprovalStatus
                        )

                        VALUES (?, ?, ?, ?)
                        """,
                        (visitor_id, name, phone, approval_status),
                    )

                    conn.commit()

                    st.success("Visitor added successfully.")

                except Exception as e:
                    st.error(f"Could not add visitor: {e}")

    elif action == "Approve / Reject Visitor":
        cursor.execute(
            """
            SELECT
                VisitorID,
                VisitorName,
                ApprovalStatus

            FROM Visitor

            ORDER BY
                VisitorName
            """
        )

        visitors = cursor.fetchall()

        visitor_options = {
            (f"{visitor_id} - {name} ({status})"): visitor_id
            for visitor_id, name, status in visitors
        }

        visitor_choice = st.selectbox("Visitor", list(visitor_options.keys()))

        new_status = st.selectbox("New Status", ["Approved", "Rejected"])

        if st.button("Update Visitor"):
            cursor.execute(
                """
                UPDATE Visitor

                SET ApprovalStatus = ?

                WHERE VisitorID = ?
                """,
                (new_status, visitor_options[visitor_choice]),
            )

            conn.commit()

            st.success("Visitor status updated.")

    elif action == "Record Visit":
        cursor.execute(
            """
            SELECT
                VisitorID,
                VisitorName

            FROM Visitor

            WHERE
                ApprovalStatus = 'Approved'

            ORDER BY
                VisitorName
            """
        )

        visitor_rows = cursor.fetchall()

        visitor_options = {
            f"{visitor_id} - {name}": visitor_id for visitor_id, name in visitor_rows
        }

        cursor.execute(
            """
            SELECT DISTINCT
                s.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                )

            FROM Student s

            JOIN Allocation a
                ON s.StudentID = a.StudentID

            WHERE
                a.Status = 'Active'

            ORDER BY
                s.StudentID
            """
        )

        student_rows = cursor.fetchall()

        student_options = {
            f"{student_id} - {name}": student_id for student_id, name in student_rows
        }

        if visitor_options and student_options:
            visitor_choice = st.selectbox("Visitor", list(visitor_options.keys()))

            student_choice = st.selectbox("Student", list(student_options.keys()))

            check_in = st.time_input("Check-in Time")

            if st.button("Record Visit"):
                cursor.execute(
                    """
                    INSERT INTO Visit
                    (
                        StudentID,
                        VisitorID,
                        CheckInTime,
                        VisitDate
                    )

                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        student_options[student_choice],
                        visitor_options[visitor_choice],
                        check_in,
                        date.today(),
                    ),
                )

                conn.commit()

                st.success("Visit recorded successfully.")

        else:
            st.warning(
                "An approved visitor and active student allocation are required."
            )

    else:
        cursor.execute(
            """
            SELECT
                v.VisitID,
                vr.VisitorName,
                v.StudentID,
                v.VisitDate,
                v.CheckInTime,
                v.CheckOutTime

            FROM Visit v

            JOIN Visitor vr
                ON v.VisitorID = vr.VisitorID

            ORDER BY
                v.VisitDate DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Visit ID",
                "Visitor Name",
                "Student ID",
                "Visit Date",
                "Check-In",
                "Check-Out",
            ],
        )

        st.dataframe(df, use_container_width=True, hide_index=True)

    cursor.close()
    conn.close()


# =====================================================
# VACANCY
# =====================================================

elif menu == "Vacancy":
    st.header("Hostel Vacancy")

    st.caption("View current hostel capacity and available spaces.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            h.HostelName,

            SUM(r.Capacity),

            SUM(
                r.CurrentOccupancy
            ),

            SUM(r.Capacity)
            -
            SUM(
                r.CurrentOccupancy
            )

        FROM Hostel h

        JOIN Block b
            ON h.HostelID = b.HostelID

        JOIN Room r
            ON b.BlockID = r.BlockID

        GROUP BY
            h.HostelID,
            h.HostelName

        ORDER BY
            4 DESC
        """
    )

    rows = cursor.fetchall()

    df = pd.DataFrame(
        rows, columns=["Hostel Name", "Capacity", "Occupied", "Vacancies"]
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    cursor.close()
    conn.close()


# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":
    st.header("Reports")

    st.caption("View summaries generated from current hostel records.")

    report = st.selectbox(
        "Select Report",
        [
            "Hostel Occupancy",
            "Hostel Vacancy",
            "Outstanding Payments",
            "Active Allocations",
        ],
    )

    conn = get_connection()
    cursor = conn.cursor()

    if report == "Hostel Occupancy":
        cursor.execute(
            """
            SELECT
                h.HostelName,

                SUM(r.Capacity),

                SUM(
                    r.CurrentOccupancy
                ),

                ROUND(
                    SUM(
                        r.CurrentOccupancy
                    )
                    /
                    NULLIF(
                        SUM(r.Capacity),
                        0
                    )
                    * 100,
                    2
                )

            FROM Hostel h

            JOIN Block b
                ON h.HostelID = b.HostelID

            JOIN Room r
                ON b.BlockID = r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName

            ORDER BY
                4 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows, columns=["Hostel", "Capacity", "Occupied", "Occupancy Rate (%)"]
        )

    elif report == "Hostel Vacancy":
        cursor.execute(
            """
            SELECT
                h.HostelName,

                SUM(r.Capacity),

                SUM(
                    r.CurrentOccupancy
                ),

                SUM(r.Capacity)
                -
                SUM(
                    r.CurrentOccupancy
                )

            FROM Hostel h

            JOIN Block b
                ON h.HostelID = b.HostelID

            JOIN Room r
                ON b.BlockID = r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName

            ORDER BY
                4 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=["Hostel", "Capacity", "Occupied", "Vacancies"])

    elif report == "Outstanding Payments":
        cursor.execute(
            """
            SELECT
                p.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                p.Balance_Due,

                p.Deadline

            FROM Payment p

            JOIN Student s
                ON p.StudentID = s.StudentID

            WHERE
                p.Balance_Due > 0

            ORDER BY
                p.Deadline
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows, columns=["Student ID", "Student Name", "Balance Due", "Deadline"]
        )

    else:
        cursor.execute(
            """
            SELECT
                a.AllocationID,

                a.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                h.HostelName,

                r.RoomNumber,

                bed.BedLabel

            FROM Allocation a

            JOIN Student s
                ON a.StudentID = s.StudentID

            JOIN Bed bed
                ON a.BedID = bed.BedID

            JOIN Room r
                ON bed.RoomID = r.RoomID

            JOIN Block b
                ON r.BlockID = b.BlockID

            JOIN Hostel h
                ON b.HostelID = h.HostelID

            WHERE
                a.Status = 'Active'

            ORDER BY
                a.AllocationID
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Allocation ID",
                "Student ID",
                "Student Name",
                "Hostel",
                "Room",
                "Bed",
            ],
        )

    st.dataframe(df, use_container_width=True, hide_index=True)

    cursor.close()
    conn.close()


# =====================================================
# ADVANCED QUERIES
# =====================================================

elif menu == "Advanced Queries":
    st.header("Advanced Queries")

    st.caption("Run advanced database queries and view their results.")

    query_choice = st.selectbox(
        "Select Query",
        [
            "1. Current Student Allocations",
            "2. Fully Occupied Rooms",
            "3. Hostel Occupancy Rates",
            "4. Outstanding Balances",
            "5. Allocations Expiring Within 30 Days",
            "6. Rank Hostels by Occupancy",
            "7. Rooms With Vacant Beds",
            "8. Students With Maintenance Requests",
            "9. Maintenance Workload by Staff",
            "10. Hostels Above 80% Occupancy",
        ],
    )

    conn = get_connection()
    cursor = conn.cursor()

    # QUERY 1
    if query_choice == "1. Current Student Allocations":
        cursor.execute(
            """
            SELECT
                s.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                s.Gender,
                s.Programme,
                s.Year,
                h.HostelName,
                b.BlockName,
                r.RoomNumber,
                bed.BedLabel,
                a.AllocationStartDate,
                a.AllocationEndDate,
                a.Status

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

            WHERE
                a.Status = 'Active'

            ORDER BY
                h.HostelName,
                b.BlockName,
                r.RoomNumber
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Student ID",
                "Student Name",
                "Gender",
                "Programme",
                "Year",
                "Hostel",
                "Block",
                "Room",
                "Bed",
                "Start Date",
                "End Date",
                "Status",
            ],
        )

    # QUERY 2
    elif query_choice == "2. Fully Occupied Rooms":
        cursor.execute(
            """
            SELECT
                r.RoomID,
                r.RoomNumber,
                r.Capacity,
                r.CurrentOccupancy,
                b.BlockName,
                h.HostelName

            FROM Room r

            JOIN Block b
                ON r.BlockID = b.BlockID

            JOIN Hostel h
                ON b.HostelID = h.HostelID

            WHERE
                r.CurrentOccupancy >= r.Capacity

            ORDER BY
                h.HostelName,
                b.BlockName,
                r.RoomNumber
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Room ID",
                "Room Number",
                "Capacity",
                "Current Occupancy",
                "Block",
                "Hostel",
            ],
        )

    # QUERY 3
    elif query_choice == "3. Hostel Occupancy Rates":
        cursor.execute(
            """
            SELECT
                h.HostelID,
                h.HostelName,
                h.Capacity,

                COALESCE(
                    SUM(r.Capacity),
                    0
                ),

                COALESCE(
                    SUM(r.CurrentOccupancy),
                    0
                ),

                ROUND(
                    COALESCE(
                        SUM(r.CurrentOccupancy),
                        0
                    )
                    /
                    NULLIF(
                        SUM(r.Capacity),
                        0
                    )
                    * 100,
                    2
                )

            FROM Hostel h

            LEFT JOIN Block b
                ON h.HostelID = b.HostelID

            LEFT JOIN Room r
                ON b.BlockID = r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName,
                h.Capacity

            ORDER BY
                6 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Hostel ID",
                "Hostel",
                "Hostel Capacity",
                "Room Capacity",
                "Current Occupancy",
                "Occupancy Rate (%)",
            ],
        )

    # QUERY 4
    elif query_choice == "4. Outstanding Balances":
        cursor.execute(
            """
            SELECT
                s.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                p.Amount_paid,
                p.Balance_Due,
                p.Deadline,
                p.Payment_Status,

                CASE
                    WHEN
                        p.Deadline < CURDATE()

                        AND
                        p.Balance_Due > 0

                    THEN 'OVERDUE'

                    WHEN
                        p.Balance_Due > 0

                    THEN 'PENDING'

                    ELSE 'PAID'

                END

            FROM Student s

            JOIN Payment p
                ON s.StudentID = p.StudentID

            WHERE
                p.Balance_Due > 0

            ORDER BY
                p.Deadline
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Student ID",
                "Student Name",
                "Amount Paid",
                "Balance Due",
                "Deadline",
                "Payment Status",
                "Payment Condition",
            ],
        )

    # QUERY 5
    elif query_choice == "5. Allocations Expiring Within 30 Days":
        cursor.execute(
            """
            SELECT
                s.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                h.HostelName,
                r.RoomNumber,
                bed.BedLabel,
                a.AllocationEndDate,

                DATEDIFF(
                    a.AllocationEndDate,
                    CURDATE()
                )

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

            WHERE
                a.Status = 'Active'

                AND
                a.AllocationEndDate
                BETWEEN
                    CURDATE()

                AND
                    DATE_ADD(
                        CURDATE(),
                        INTERVAL 30 DAY
                    )

            ORDER BY
                a.AllocationEndDate
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Student ID",
                "Student Name",
                "Hostel",
                "Room",
                "Bed",
                "End Date",
                "Days Remaining",
            ],
        )

    # QUERY 6
    elif query_choice == "6. Rank Hostels by Occupancy":
        cursor.execute(
            """
            WITH HostelOccupancy AS
            (
                SELECT
                    h.HostelID,
                    h.HostelName,

                    COALESCE(
                        SUM(r.Capacity),
                        0
                    )
                    AS TotalCapacity,

                    COALESCE(
                        SUM(r.CurrentOccupancy),
                        0
                    )
                    AS OccupiedBeds

                FROM Hostel h

                LEFT JOIN Block b
                    ON h.HostelID = b.HostelID

                LEFT JOIN Room r
                    ON b.BlockID = r.BlockID

                GROUP BY
                    h.HostelID,
                    h.HostelName
            )

            SELECT
                HostelID,
                HostelName,
                TotalCapacity,
                OccupiedBeds,

                ROUND(
                    OccupiedBeds
                    /
                    NULLIF(
                        TotalCapacity,
                        0
                    )
                    * 100,
                    2
                ),

                RANK() OVER
                (
                    ORDER BY
                        OccupiedBeds
                        /
                        NULLIF(
                            TotalCapacity,
                            0
                        )
                    DESC
                )

            FROM HostelOccupancy
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Hostel ID",
                "Hostel",
                "Total Capacity",
                "Occupied Beds",
                "Occupancy Rate (%)",
                "Rank",
            ],
        )

    # QUERY 7
    elif query_choice == "7. Rooms With Vacant Beds":
        cursor.execute(
            """
            SELECT
                h.HostelName,
                b.BlockName,
                r.RoomNumber,
                r.Capacity,

                COUNT(
                    bed.BedID
                ),

                SUM(
                    CASE

                        WHEN
                            bed.Status = 'Vacant'

                        THEN 1

                        ELSE 0

                    END
                )

            FROM Hostel h

            JOIN Block b
                ON h.HostelID = b.HostelID

            JOIN Room r
                ON b.BlockID = r.BlockID

            JOIN Bed bed
                ON r.RoomID = bed.RoomID

            GROUP BY
                h.HostelName,
                b.BlockName,
                r.RoomNumber,
                r.Capacity

            HAVING

                SUM(
                    CASE
                        WHEN
                            bed.Status = 'Vacant'

                        THEN 1

                        ELSE 0
                    END
                ) > 0

            ORDER BY
                6 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Hostel",
                "Block",
                "Room",
                "Capacity",
                "Total Beds",
                "Vacant Beds",
            ],
        )

    # QUERY 8
    elif query_choice == "8. Students With Maintenance Requests":
        cursor.execute(
            """
            SELECT
                s.StudentID,

                CONCAT(
                    s.FirstName,
                    ' ',
                    s.LastName
                ),

                m.MaintenanceID,
                r.RoomNumber,
                m.IssueDescription,
                m.RequestDate,
                m.Status,
                m.DateResolved

            FROM Student s

            JOIN Maintenance m
                ON s.StudentID = m.StudentID

            JOIN Room r
                ON m.RoomID = r.RoomID

            ORDER BY
                m.RequestDate DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Student ID",
                "Student Name",
                "Maintenance ID",
                "Room",
                "Issue",
                "Request Date",
                "Status",
                "Date Resolved",
            ],
        )

    # QUERY 9
    elif query_choice == "9. Maintenance Workload by Staff":
        cursor.execute(
            """
            SELECT
                st.StaffID,

                CONCAT(
                    st.First_Name,
                    ' ',
                    st.Last_Name
                ),

                st.Email,

                COUNT(
                    m.MaintenanceID
                ),

                SUM(
                    CASE
                        WHEN
                            m.Status = 'Resolved'

                        THEN 1

                        ELSE 0
                    END
                ),

                SUM(
                    CASE
                        WHEN
                            m.MaintenanceID
                            IS NOT NULL

                            AND
                            m.Status <> 'Resolved'

                        THEN 1

                        ELSE 0
                    END
                )

            FROM Staff st

            LEFT JOIN Maintenance m
                ON st.StaffID = m.StaffID

            GROUP BY
                st.StaffID,
                st.First_Name,
                st.Last_Name,
                st.Email

            ORDER BY
                6 DESC,
                4 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Staff ID",
                "Staff Name",
                "Email",
                "Total Requests",
                "Resolved",
                "Outstanding",
            ],
        )

    # QUERY 10
    else:
        cursor.execute(
            """
            SELECT
                h.HostelID,
                h.HostelName,

                SUM(
                    r.Capacity
                ),

                SUM(
                    r.CurrentOccupancy
                ),

                ROUND(
                    SUM(
                        r.CurrentOccupancy
                    )
                    /
                    NULLIF(
                        SUM(r.Capacity),
                        0
                    )
                    * 100,
                    2
                )

            FROM Hostel h

            JOIN Block b
                ON h.HostelID = b.HostelID

            JOIN Room r
                ON b.BlockID = r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName

            HAVING

                ROUND(
                    SUM(
                        r.CurrentOccupancy
                    )
                    /
                    NULLIF(
                        SUM(r.Capacity),
                        0
                    )
                    * 100,
                    2
                ) > 80

            ORDER BY
                5 DESC
            """
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Hostel ID",
                "Hostel",
                "Total Capacity",
                "Occupied Beds",
                "Occupancy (%)",
            ],
        )

    if df.empty:
        st.info("No records matched this query.")

    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    cursor.close()
    conn.close()


# =====================================================
# LOGOUT
# =====================================================

st.sidebar.divider()


if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.clear()

    st.switch_page("Dashboard.py")
