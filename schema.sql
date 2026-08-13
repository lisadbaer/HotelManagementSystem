CREATE DATABASE Hostel_Management;
USE Hostel_Management;

CREATE TABLE Hostel (
    HostelID varchar(10) primary key,
    HostelName varchar(100) not null,
    Location varchar(100) not null,
    Capacity int not null,
    GenderType ENUM ('Male', 'Female') not null
);

Create table Staff(
    StaffID varchar(10) primary key,
    First_Name varchar(50) not null,
    Last_Name varchar(50) not null,
    Phone varchar(10) not null,
    Email varchar(100) not null unique
);

CREATE TABLE SEMESTER (
    SemesterID VARCHAR(10) PRIMARY KEY,
    AcademicYear VARCHAR(10) not null,
    SemesterName VARCHAR(50) not null,
    StartDate DATE not null,
    EndDate DATE not null CHECK(EndDate > StartDate)
);

create table Student(
    StudentID varchar(8) primary key,
    FirstName varchar(25) not null,
    LastName varChar(25) not null,
    Gender Enum('Female','Male') not null,
    DateOfBirth date not null,
    Phone varChar(10) not null,
    Email varchar(60) not null,
    Programme Enum('CS','BA','ENG','LLB') not null,
    Class int not null
);

Create table Manager(
    ManagerID varchar(10) primary key,
    StaffID varchar(10) not null unique,
    AssignedHostel varchar(10) not null unique,
    foreign key (StaffID) references Staff(StaffID),
    foreign key (AssignedHostel) references Hostel(HostelID)
);

Create table Auxiliary_Staff(
    AuxiliaryID varchar(10) primary key,
    StaffID varchar(10) NOT NULL UNIQUE,
    Role varchar(30) not null,
    foreign key (StaffID) references Staff(StaffID)
);

create table Block (
    BlockID varchar(10) primary key,
    BlockName varchar(100) not null,
    HostelID varchar(10) not null,
    No_of_Floors int not null,
    foreign key (HostelID) references Hostel(HostelID)
);

create table Room (
    RoomID varchar(10) primary key,
    RoomNumber varchar(20) not null,
    Floor int not null,
    Capacity int not null,
    BlockID varchar(10) not null,
    CurrentOccupancy int not null default 0,
    foreign key(BlockID) references Block(BlockID),
    check (CurrentOccupancy >= 0),
    check (CurrentOccupancy <= Capacity)
);

create table Bed(
    BedID varchar(10) primary key,
    BedLabel varchar(10) not null,
    Status ENUM ('Vacant','Occupied','Reserved') not null,
    RoomID varchar(10) not null,
    foreign key (RoomID) references Room(RoomID)
);

create table Visitor(
    VisitorID varchar(10) primary key,
    VisitorName varchar(120) not null,
    Phone varChar(20) not null,
    ApprovalStatus Enum ('Approved','Rejected') not null
);

create table Visit(
    VisitID int auto_increment primary key,
    StudentID varChar(8) not null,
    CheckInTime time,
    CheckOutTime time,
    VisitDate date,
    foreign key (StudentID) references Student(StudentID),
    foreign key (VisitorID) references Visitor(VisitorID)
);

create table Allocation(
    AllocationID varChar(6) primary key,
    StudentID varChar(8) not null,
    BedID varChar(10) not null,
    SemesterID  varChar(10) not null,
    AllocationStartDate date not null,
    AllocationEndDate date not null,
    OfferSentDate date not null,
    AcceptanceDeadline date not null,
    AcceptedDate date null,
    Status Enum('Active','Inactive','Declined', 'Pending') not null default 'Pending',
    foreign key (StudentID) references Student(StudentID),
    foreign key (BedID) references Bed(BedID),
    foreign key (SemesterID) references Semester(SemesterID),
    check (AllocationStartDate <= AllocationEndDate)
);

CREATE TABLE MAINTENANCE (
    MaintenanceID VARCHAR(10) PRIMARY KEY,
    RoomID VARCHAR(10),
    StudentID VARCHAR(8),
    StaffID VARCHAR(10),
    ManagerID VARCHAR(10),
    IssueDescription VARCHAR(255),
    RequestDate DATE,
    Status Enum('Resolved','Pending','Ok'),
    DateResolved DATE,
    foreign key (RoomID) references ROOM(RoomID),
    foreign key (StudentID) references STUDENT(StudentID),
    foreign key (StaffID) references STAFF(StaffID),
    foreign key (ManagerID) references MANAGER(ManagerID)
);

create table Inspection(
    InspectionID varchar(10) primary key,
    RoomID varchar(10) NOT NULL,
    ManagerID varchar(10) NOT NULL,
    InspectionDate date NOT NULL,
    RoomCondition varchar(20) NOT NULL,
    Remarks varchar(255),
    foreign key(RoomID) references Room(RoomID),
    foreign key(ManagerID) references Manager(ManagerID)
);

CREATE TABLE Payment (
    PaymentID VARCHAR(10) PRIMARY KEY,
    AllocationID VARCHAR(6) not null,
    StudentID VARCHAR(8) not null,
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

ALTER TABLE Student
ADD UserID INT UNIQUE,
ADD FOREIGN KEY (UserID)
REFERENCES UserAccount(UserID);

ALTER TABLE Manager
ADD UserID INT UNIQUE,
ADD FOREIGN KEY (UserID)
REFERENCES UserAccount(UserID);