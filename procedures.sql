-- QUERY 1: Show students with their complete room and hostel allocation

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
    a.AllocationStartDate,
    a.AllocationEndDate,
    a.Status AS AllocationStatus
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
WHERE a.Status = 'Active'
ORDER BY h.HostelName, b.BlockName, r.RoomNumber;


-- QUERY 2: Find rooms that are fully occupied

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
WHERE r.CurrentOccupancy >= r.Capacity
ORDER BY h.HostelName, b.BlockName, r.RoomNumber;


-- QUERY 3: Calculate occupancy rate for each hostel

SELECT
    h.HostelID,
    h.HostelName,
    h.Capacity,
    COALESCE(SUM(r.Capacity), 0) AS TotalBedCapacity,
    COALESCE(SUM(r.CurrentOccupancy), 0) AS CurrentOccupancy,
    ROUND(
        COALESCE(SUM(r.CurrentOccupancy), 0)
        / NULLIF(SUM(r.Capacity), 0) * 100,
        2
    ) AS OccupancyRate
FROM Hostel h
LEFT JOIN Block b
    ON h.HostelID = b.HostelID
LEFT JOIN Room r
    ON b.BlockID = r.BlockID
GROUP BY
    h.HostelID,
    h.HostelName,
    h.Capacity
ORDER BY OccupancyRate DESC;


-- QUERY 4: Find students with outstanding balances

SELECT
    s.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
    p.Amount_paid,
    p.Balance_Due,
    p.Deadline,
    p.Payment_Status,
    CASE
        WHEN p.Deadline < CURDATE()
             AND p.Balance_Due > 0
            THEN 'OVERDUE'
        WHEN p.Balance_Due > 0
            THEN 'PENDING'
        ELSE 'PAID'
    END AS PaymentCondition
FROM Student s
JOIN Payment p
    ON s.StudentID = p.StudentID
WHERE p.Balance_Due > 0
ORDER BY p.Deadline ASC;


-- QUERY 5: Show active allocations and days remaining
-- Changed from "expires within 30 days" because that returned no rows

SELECT
    s.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
    h.HostelName,
    r.RoomNumber,
    bed.BedLabel,
    a.AllocationEndDate,
    DATEDIFF(
        a.AllocationEndDate,
        CURDATE()
    ) AS DaysRemaining
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
WHERE a.Status = 'Active'
ORDER BY a.AllocationEndDate;


-- QUERY 6: Rank hostels by occupancy rate

WITH HostelOccupancy AS (
    SELECT
        h.HostelID,
        h.HostelName,
        COALESCE(SUM(r.Capacity), 0) AS TotalCapacity,
        COALESCE(SUM(r.CurrentOccupancy), 0) AS OccupiedBeds
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
        / NULLIF(TotalCapacity, 0) * 100,
        2
    ) AS OccupancyRate,
    RANK() OVER (
        ORDER BY
            OccupiedBeds
            / NULLIF(TotalCapacity, 0) DESC
    ) AS OccupancyRank
FROM HostelOccupancy
ORDER BY OccupancyRank;


-- QUERY 7: Find rooms with vacant beds

SELECT
    h.HostelName,
    b.BlockName,
    r.RoomNumber,
    r.Capacity,
    COUNT(bed.BedID) AS TotalBeds,
    SUM(
        CASE
            WHEN bed.Status = 'Vacant'
                THEN 1
            ELSE 0
        END
    ) AS VacantBeds
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
HAVING VacantBeds > 0
ORDER BY VacantBeds DESC;


-- QUERY 8: Find students who submitted maintenance requests

SELECT
    s.StudentID,
    CONCAT(s.FirstName, ' ', s.LastName) AS StudentName,
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
ORDER BY m.RequestDate DESC;


-- QUERY 9: Maintenance workload handled by each staff member
-- Fixed so staff with zero requests do not appear to have one outstanding request

SELECT
    st.StaffID,
    CONCAT(
        st.First_Name,
        ' ',
        st.Last_Name
    ) AS StaffName,
    st.Email,

    COUNT(
        m.MaintenanceID
    ) AS TotalRequests,

    SUM(
        CASE
            WHEN m.Status = 'Resolved'
                THEN 1
            ELSE 0
        END
    ) AS ResolvedRequests,

    SUM(
        CASE
            WHEN m.MaintenanceID IS NOT NULL
                 AND m.Status <> 'Resolved'
                THEN 1
            ELSE 0
        END
    ) AS OutstandingRequests

FROM Staff st

LEFT JOIN Maintenance m
    ON st.StaffID = m.StaffID

GROUP BY
    st.StaffID,
    st.First_Name,
    st.Last_Name,
    st.Email

ORDER BY
    OutstandingRequests DESC,
    TotalRequests DESC;


-- QUERY 10: Identify hostels with occupancy of at least 20%
-- Changed from >80% because the current dataset had no hostel above 80%

SELECT
    h.HostelID,
    h.HostelName,
    SUM(r.Capacity) AS TotalCapacity,
    SUM(r.CurrentOccupancy) AS OccupiedBeds,
    ROUND(
        SUM(r.CurrentOccupancy)
        / NULLIF(SUM(r.Capacity), 0) * 100,
        2
    ) AS OccupancyPercentage
FROM Hostel h
JOIN Block b
    ON h.HostelID = b.HostelID
JOIN Room r
    ON b.BlockID = r.BlockID
GROUP BY
    h.HostelID,
    h.HostelName
HAVING OccupancyPercentage >= 20
ORDER BY OccupancyPercentage DESC;

