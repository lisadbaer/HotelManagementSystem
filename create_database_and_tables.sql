

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