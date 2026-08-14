
CREATE OR REPLACE VIEW vw_CurrentStudentAllocations AS
SELECT
    s.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
    s.Gender,
    s.Programme,
    s.Year,
    h.HostelName,
    b.BlockName,
    r.RoomNumber,
    bed.BedLabel,
    a.SemesterID,
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
WHERE a.Status = 'Active';


CREATE OR REPLACE VIEW vw_HostelOccupancy AS
SELECT
    h.HostelID,
    h.HostelName,
    h.GenderType,
    h.Capacity AS HostelCapacity,
    COALESCE(SUM(r.Capacity), 0) AS RoomCapacity,
    COALESCE(SUM(r.CurrentOccupancy), 0) AS CurrentOccupancy,
    ROUND(
        COALESCE(SUM(r.CurrentOccupancy), 0)
        / NULLIF(SUM(r.Capacity), 0) * 100,
        2
    ) AS OccupancyPercentage
FROM Hostel h
LEFT JOIN Block b
    ON h.HostelID = b.HostelID
LEFT JOIN Room r
    ON b.BlockID = r.BlockID
GROUP BY
    h.HostelID,
    h.HostelName,
    h.GenderType,
    h.Capacity;


CREATE OR REPLACE VIEW vw_OutstandingPayments AS
SELECT
    p.PaymentID,
    p.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
    p.Amount_paid,
    p.Balance_Due,
    p.Payment_Date,
    p.Deadline,
    CASE
        WHEN p.Deadline < CURDATE()
             AND p.Balance_Due > 0
        THEN 'Overdue'

        WHEN p.Balance_Due > 0
        THEN 'Pending'

        ELSE 'Paid'
    END AS PaymentCondition
FROM Payment p
JOIN Student s
    ON p.StudentID = s.StudentID
WHERE p.Balance_Due > 0;


CREATE OR REPLACE VIEW vw_MaintenanceSummary AS
SELECT
    m.MaintenanceID,
    m.RoomID,
    r.RoomNumber,
    m.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
    m.StaffID,
    CONCAT(st.First_Name, ' ', st.Last_Name) AS StaffName,
    m.IssueDescription,
    m.RequestDate,
    m.Status,
    m.DateResolved
FROM Maintenance m
JOIN Room r
    ON m.RoomID = r.RoomID
LEFT JOIN Student s
    ON m.StudentID = s.StudentID
LEFT JOIN Staff st
    ON m.StaffID = st.StaffID;


CREATE OR REPLACE VIEW vw_AvailableBeds AS
SELECT
    bed.BedID,
    bed.BedLabel,
    r.RoomID,
    r.RoomNumber,
    r.Floor,
    b.BlockID,
    b.BlockName,
    h.HostelID,
    h.HostelName,
    h.GenderType
FROM Bed bed
JOIN Room r
    ON bed.RoomID = r.RoomID
JOIN Block b
    ON r.BlockID = b.BlockID
JOIN Hostel h
    ON b.HostelID = h.HostelID
WHERE bed.Status = 'Vacant';