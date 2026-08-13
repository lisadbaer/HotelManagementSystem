import streamlit as st
from database import get_connection
from backup import create_backup
from datetime import date, timedelta


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

st.title("Manager Dashboard")


menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Allocations",
        "Inspections",
        "Maintenance",
        "Student Payments",
        "Visitors",
        "Vacancy",
        "Reports",
    ],
)


# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":
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

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", students)

    c2.metric("Rooms", rooms)

    c3.metric("Active Allocations", allocations)

    c4.metric("Vacant Beds", vacant_beds)

    st.divider()

    st.subheader("Database Backup")

    if st.button("Backup Database"):
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

    action = st.radio("Action", ["Give Allocation", "Remove Allocation"])

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

        # Correct-gender vacant beds
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
                ON b.HostelID =
                   h.HostelID

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
            (f"{bed_id} - {hostel}, Room {room}, Bed {label}"): bed_id
            for bed_id, hostel, room, label in bed_rows
        }

        if not bed_options:
            st.warning("No suitable vacant beds are available.")

        else:
            bed_choice = st.selectbox("Available Bed", list(bed_options.keys()))

            bed_id = bed_options[bed_choice]

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

            if st.button("Give Allocation"):
                try:
                    conn.autocommit = False

                    # Existing active allocation
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
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active')
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
                                  AND Status = 'Occupied'
                            )

                            WHERE RoomID = ?
                            """,
                            (room_id, room_id),
                        )

                        conn.commit()

                        st.success(f"Allocation {allocation_id} created.")

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
                ON a.StudentID =
                   s.StudentID

            WHERE
                a.Status = 'Active'

            ORDER BY
                a.AllocationID
            """
        )

        rows = cursor.fetchall()

        options = {
            (f"{allocation_id} - {student_id} - {name}"): (allocation_id, bed_id)
            for allocation_id, student_id, name, bed_id in rows
        }

        if not options:
            st.info("No active allocations.")

        else:
            selected = st.selectbox("Allocation", list(options.keys()))

            allocation_id, bed_id = options[selected]

            if st.button("Remove Allocation"):
                try:
                    conn.autocommit = False

                    # Keep historical record
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

    action = st.selectbox(
        "Action", ["View Inspections", "Add Inspection", "Update Inspection"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    # VIEW
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

        st.dataframe(cursor.fetchall(), use_container_width=True)

    # ADD
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

        condition = st.selectbox("Room Condition", ["Good", "Fair", "Poor"])

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

    # UPDATE
    else:
        cursor.execute(
            """
            SELECT InspectionID
            FROM Inspection
            ORDER BY InspectionID
            """
        )

        ids = [row[0] for row in cursor.fetchall()]

        inspection_id = st.selectbox("Inspection", ids)

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

            st.success("Inspection updated.")

    cursor.close()
    conn.close()


# =====================================================
# MAINTENANCE
# =====================================================

elif menu == "Maintenance":
    st.header("Maintenance Management")

    action = st.selectbox(
        "Action", ["View Maintenance", "Add Maintenance", "Update Maintenance"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    # VIEW
    if action == "View Maintenance":
        cursor.execute(
            """
            SELECT
                m.MaintenanceID,
                m.RoomID,
                m.StudentID,
                m.StaffID,
                m.ManagerID,
                m.IssueDescription,
                m.RequestDate,
                m.Status,
                m.DateResolved

            FROM Maintenance m

            ORDER BY
                m.RequestDate DESC
            """
        )

        st.dataframe(cursor.fetchall(), use_container_width=True)

    # ADD
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

                VALUES (?, ?, ?, ?, ?, 'Pending')
                """,
                (maintenance_id, room_id, manager_id, issue, date.today()),
            )

            conn.commit()

            st.success(f"Maintenance record {maintenance_id} added.")

    # UPDATE
    else:
        cursor.execute(
            """
            SELECT MaintenanceID
            FROM Maintenance
            ORDER BY MaintenanceID
            """
        )

        maintenance_ids = [row[0] for row in cursor.fetchall()]

        maintenance_id = st.selectbox("Maintenance ID", maintenance_ids)

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
                ON a.StaffID =
                   s.StaffID

            WHERE
                a.Role =
                'Maintenance'

            ORDER BY
                s.First_Name
            """
        )

        maintenance_staff = cursor.fetchall()

        staff_options = {
            f"{staff_id} - {name}": staff_id for staff_id, name in maintenance_staff
        }

        selected_staff = st.selectbox("Maintenance Staff", list(staff_options.keys()))

        staff_id = staff_options[selected_staff]

        status = st.selectbox("Status", ["Pending", "Resolved", "Ok"])

        issue = st.text_area("Updated Issue Description")

        if st.button("Update Maintenance"):
            resolved_date = None

            if status == "Resolved":
                resolved_date = date.today()

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
                (staff_id, manager_id, issue, status, resolved_date, maintenance_id),
            )

            conn.commit()

            st.success("Maintenance record updated.")

    cursor.close()
    conn.close()


# =====================================================
# STUDENT PAYMENTS
# =====================================================

elif menu == "Student Payments":
    st.header("Student Payments")

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
            ) AS StudentName,

            p.Amount_paid,
            p.Payment_Date,
            p.Payment_Method,
            p.Payment_Status,
            p.Balance_Due,
            p.Deadline

        FROM Payment p

        JOIN Student s
            ON p.StudentID =
               s.StudentID

        WHERE p.StudentID LIKE ?

        ORDER BY
            p.Payment_Date DESC
        """,
        (f"%{search}%",),
    )

    st.dataframe(cursor.fetchall(), use_container_width=True)

    cursor.close()
    conn.close()


# =====================================================
# VISITORS
# =====================================================

elif menu == "Visitors":
    st.header("Visitor Management")

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

    # VIEW VISITORS
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

        st.dataframe(cursor.fetchall(), use_container_width=True)

    # ADD VISITOR
    elif action == "Add Visitor":
        visitor_id = st.text_input("Visitor ID")

        name = st.text_input("Visitor Name")

        phone = st.text_input("Phone")

        if st.button("Add Visitor"):
            cursor.execute(
                """
                INSERT INTO Visitor
                (
                    VisitorID,
                    VisitorName,
                    Phone,
                    ApprovalStatus
                )

                VALUES (?, ?, ?, 'Approved')
                """,
                (visitor_id, name, phone),
            )

            conn.commit()

            st.success("Visitor added.")

    # APPROVE / REJECT
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

        options = {
            (f"{visitor_id} - {name} ({status})"): visitor_id
            for visitor_id, name, status in visitors
        }

        selected = st.selectbox("Visitor", list(options.keys()))

        status = st.selectbox("Status", ["Approved", "Rejected"])

        if st.button("Update Visitor"):
            cursor.execute(
                """
                UPDATE Visitor

                SET ApprovalStatus = ?

                WHERE VisitorID = ?
                """,
                (status, options[selected]),
            )

            conn.commit()

            st.success("Visitor status updated.")

    # RECORD VISIT
    elif action == "Record Visit":
        cursor.execute(
            """
            SELECT
                VisitorID,
                VisitorName

            FROM Visitor

            WHERE
                ApprovalStatus =
                'Approved'

            ORDER BY
                VisitorName
            """
        )

        visitor_rows = cursor.fetchall()

        visitor_options = {f"{vid} - {name}": vid for vid, name in visitor_rows}

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
                ON s.StudentID =
                   a.StudentID

            WHERE
                a.Status =
                'Active'

            ORDER BY
                s.StudentID
            """
        )

        student_rows = cursor.fetchall()

        student_options = {f"{sid} - {name}": sid for sid, name in student_rows}

        if visitor_options and student_options:
            visitor = st.selectbox("Visitor", list(visitor_options.keys()))

            student = st.selectbox("Student", list(student_options.keys()))

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
                        student_options[student],
                        visitor_options[visitor],
                        check_in,
                        date.today(),
                    ),
                )

                conn.commit()

                st.success("Visit recorded.")

    # VIEW VISITS
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
                ON v.VisitorID =
                   vr.VisitorID

            ORDER BY
                v.VisitDate DESC
            """
        )

        st.dataframe(cursor.fetchall(), use_container_width=True)

    cursor.close()
    conn.close()


# =====================================================
# VACANCY
# =====================================================

elif menu == "Vacancy":
    st.header("Hostel Vacancy")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            h.HostelName,

            SUM(r.Capacity)
                AS TotalCapacity,

            SUM(r.CurrentOccupancy)
                AS Occupied,

            SUM(r.Capacity)
            -
            SUM(r.CurrentOccupancy)
                AS Vacancies

        FROM Hostel h

        JOIN Block b
            ON h.HostelID =
               b.HostelID

        JOIN Room r
            ON b.BlockID =
               r.BlockID

        GROUP BY
            h.HostelID,
            h.HostelName

        ORDER BY
            Vacancies DESC
        """
    )

    st.dataframe(cursor.fetchall(), use_container_width=True)

    cursor.close()
    conn.close()


# =====================================================
# REPORTS
# =====================================================

elif menu == "Reports":
    st.header("Reports")

    report = st.selectbox(
        "Report",
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
                SUM(r.Capacity)
                    AS Capacity,
                SUM(r.CurrentOccupancy)
                    AS Occupied,

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
                    AS OccupancyRate

            FROM Hostel h

            JOIN Block b
                ON h.HostelID =
                   b.HostelID

            JOIN Room r
                ON b.BlockID =
                   r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName

            ORDER BY
                OccupancyRate DESC
            """
        )

    elif report == "Hostel Vacancy":
        cursor.execute(
            """
            SELECT
                h.HostelName,

                SUM(r.Capacity)
                    AS Capacity,

                SUM(r.CurrentOccupancy)
                    AS Occupied,

                SUM(r.Capacity)
                -
                SUM(r.CurrentOccupancy)
                    AS Vacancies

            FROM Hostel h

            JOIN Block b
                ON h.HostelID =
                   b.HostelID

            JOIN Room r
                ON b.BlockID =
                   r.BlockID

            GROUP BY
                h.HostelID,
                h.HostelName

            ORDER BY
                Vacancies DESC
            """
        )

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
                ON p.StudentID =
                   s.StudentID

            WHERE
                p.Balance_Due > 0

            ORDER BY
                p.Deadline
            """
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
                ON a.StudentID =
                   s.StudentID

            JOIN Bed bed
                ON a.BedID =
                   bed.BedID

            JOIN Room r
                ON bed.RoomID =
                   r.RoomID

            JOIN Block b
                ON r.BlockID =
                   b.BlockID

            JOIN Hostel h
                ON b.HostelID =
                   h.HostelID

            WHERE
                a.Status =
                'Active'

            ORDER BY
                a.AllocationID
            """
        )

    st.dataframe(cursor.fetchall(), use_container_width=True)

    cursor.close()
    conn.close()


# =====================================================
# LOGOUT
# =====================================================

st.sidebar.divider()

if st.sidebar.button("Logout"):
    st.session_state.clear()

    st.switch_page("app.py")
