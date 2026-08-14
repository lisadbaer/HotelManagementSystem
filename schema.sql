

CREATE DATABASE Hostel_Management;
USE Hostel_Management;

CREATE TABLE Hostel (
    HostelID VARCHAR(10) PRIMARY KEY,
    HostelName VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL,
    GenderType ENUM('Male','Female') NOT NULL
);

CREATE TABLE Staff (
    StaffID VARCHAR(10) PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Semester (
    SemesterID VARCHAR(10) PRIMARY KEY,
    AcademicYear VARCHAR(10) NOT NULL,
    SemesterName VARCHAR(50) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    CHECK (EndDate > StartDate)
);

CREATE TABLE Student (
    StudentID VARCHAR(8) PRIMARY KEY,
    FirstName VARCHAR(25) NOT NULL,
    LastName VARCHAR(25) NOT NULL,
    Gender ENUM('Female','Male') NOT NULL,
    DateOfBirth DATE NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Email VARCHAR(60) NOT NULL,
    Programme ENUM('CS','BA','ENG','LLB') NOT NULL,
    Year INT NOT NULL
);

CREATE TABLE Manager (
    ManagerID VARCHAR(10) PRIMARY KEY,
    StaffID VARCHAR(10) NOT NULL UNIQUE,
    AssignedHostel VARCHAR(10) NOT NULL,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (AssignedHostel) REFERENCES Hostel(HostelID)
);

CREATE TABLE Auxiliary_Staff (
    AuxiliaryID VARCHAR(10) PRIMARY KEY,
    StaffID VARCHAR(10) NOT NULL UNIQUE,
    Role VARCHAR(30) NOT NULL,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

CREATE TABLE Block (
    BlockID VARCHAR(10) PRIMARY KEY,
    BlockName VARCHAR(100) NOT NULL,
    HostelID VARCHAR(10) NOT NULL,
    No_of_Floors INT NOT NULL,
    FOREIGN KEY (HostelID) REFERENCES Hostel(HostelID)
);

CREATE TABLE Room (
    RoomID VARCHAR(10) PRIMARY KEY,
    RoomNumber VARCHAR(20) NOT NULL,
    Floor INT NOT NULL,
    Capacity INT NOT NULL,
    BlockID VARCHAR(10) NOT NULL,
    CurrentOccupancy INT NOT NULL DEFAULT 0,
    FOREIGN KEY (BlockID) REFERENCES Block(BlockID),
    CHECK (CurrentOccupancy >= 0),
    CHECK (CurrentOccupancy <= Capacity)
);

CREATE TABLE Bed (
    BedID VARCHAR(10) PRIMARY KEY,
    BedLabel VARCHAR(10) NOT NULL,
    Status ENUM('Vacant','Occupied','Reserved') NOT NULL,
    RoomID VARCHAR(10) NOT NULL,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Visitor (
    VisitorID VARCHAR(10) PRIMARY KEY,
    VisitorName VARCHAR(120) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    ApprovalStatus ENUM('Approved','Rejected') NOT NULL
);

CREATE TABLE Visit (
    VisitID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID VARCHAR(8) NOT NULL,
    VisitorID VARCHAR(10) NOT NULL,
    CheckInTime TIME,
    CheckOutTime TIME,
    VisitDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (VisitorID) REFERENCES Visitor(VisitorID)
);

CREATE TABLE Allocation (
    AllocationID VARCHAR(6) PRIMARY KEY,
    StudentID VARCHAR(8) NOT NULL,
    BedID VARCHAR(10) NOT NULL,
    SemesterID VARCHAR(10) NOT NULL,
    AllocationStartDate DATE NOT NULL,
    AllocationEndDate DATE NOT NULL,
    OfferSentDate DATE NOT NULL,
    AcceptanceDeadline DATE NOT NULL,
    AcceptedDate DATE NULL,
    Status ENUM('Active','Inactive','Declined','Pending') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (BedID) REFERENCES Bed(BedID),
    FOREIGN KEY (SemesterID) REFERENCES Semester(SemesterID),
    CHECK (AllocationStartDate <= AllocationEndDate)
);

CREATE TABLE Maintenance (
    MaintenanceID VARCHAR(10) PRIMARY KEY,
    RoomID VARCHAR(10),
    StudentID VARCHAR(8),
    StaffID VARCHAR(10),
    ManagerID VARCHAR(10),
    IssueDescription VARCHAR(255),
    RequestDate DATE,
    Status ENUM('Resolved','Pending','Ok'),
    DateResolved DATE,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (ManagerID) REFERENCES Manager(ManagerID)
);

CREATE TABLE Inspection (
    InspectionID VARCHAR(10) PRIMARY KEY,
    RoomID VARCHAR(10) NOT NULL,
    ManagerID VARCHAR(10) NOT NULL,
    Inspection_date DATE NOT NULL,
    RoomCondition VARCHAR(20) NOT NULL,
    Remarks VARCHAR(255),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
    FOREIGN KEY (ManagerID) REFERENCES Manager(ManagerID)
);

CREATE TABLE Payment (
    PaymentID VARCHAR(10) PRIMARY KEY,
    AllocationID VARCHAR(6) NOT NULL,
    StudentID VARCHAR(8) NOT NULL,
    Amount_paid DECIMAL(10,2) NOT NULL CHECK (Amount_paid > 0),
    Payment_Date DATE NOT NULL,
    Payment_Method VARCHAR(20) NOT NULL,
    Payment_Status ENUM('Pending','Paid') NOT NULL,
    Balance_Due DECIMAL(10,2) NOT NULL CHECK (Balance_Due >= 0),
    Deadline DATE NOT NULL,
    FOREIGN KEY (AllocationID) REFERENCES Allocation(AllocationID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);

Advanced Queries:


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


create role HostelManager;
create role MaintenanceOfficer;
create role SecurityOfficer;

grant select on hostel_project.room to MaintenanceOfficer;
grant select on hostel_project.maintenance to MaintenanceOfficer;

grant select, insert, update on hostel_project.maintenance to MaintenanceOfficer;
grant select on hostel_project.student to SecurityOfficer;

grant select, insert,update on hostel_project.visitor to SecurityOfficer;
grant select, insert,update on hostel_project.visit to SecurityOfficer;

grant all privileges on hostel_project.* to HostelManager;

CREATE USER 'manager1'@'localhost' IDENTIFIED BY 'Manager!';

CREATE USER 'maintenance1'@'localhost'IDENTIFIED BY 'Maintenance!';

CREATE USER 'security1'@'localhost'IDENTIFIED BY 'Security';



GRANT HostelManager TO 'manager1'@'localhost';

GRANT MaintenanceOfficer 'maintenance1'@'localhost';

GRANT SecurityOfficer TO 'security1'@'localhost';


SET DEFAULT ROLE HostelManager FOR 'manager1'@'localhost';

SET DEFAULT ROLE MaintenanceOfficer FOR 'maintenance1'@'localhost';

SET DEFAULT ROLE SecurityOfficer FOR 'security1'@'localhost';