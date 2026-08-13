INSERT INTO Hostel
(HostelID, HostelName, Location, Capacity, GenderType)
VALUES
('H1', 'Araba Hostel', 'North Campus', 12, 'Female'),
('H2', 'Johnson Hostel', 'East Campus', 14, 'Male'),
('H3', 'Henry Hostel', 'West Campus', 12, 'Female'),
('H4', 'Akua Hostel', 'South Campus', 12, 'Male');

INSERT INTO Staff
(StaffID, First_Name, Last_Name, Phone, Email)
VALUES
('SF1', 'Rita', 'Johnson', '0233768578', 'rita@hostel.edu.gh'),
('SF2', 'Ama', 'Forb', '0256789465', 'ama@hostel.edu.gh'),
('SF3', 'Kweku', 'Ahyei', '0214356479', 'kweku@hostel.edu.gh'),
('SF4', 'Daniel', 'Mensah', '0245123789', 'daniel@hostel.edu.gh'),
('SF5', 'Grace', 'Owusu', '0209876543', 'grace@hostel.edu.gh'),
('SF6', 'Michael', 'Boateng', '0551234567', 'michael@hostel.edu.gh'),
('SF7', 'Linda', 'Adjei', '0543456789', 'linda@hostel.edu.gh'),
('SF8', 'Kwame', 'Asare', '0503456789', 'kwame@hostel.edu.gh'),
('SF9', 'Esther', 'Osei', '0244567890', 'esther@hostel.edu.gh'),
('SF10', 'Samuel', 'Amoah', '0555678901', 'samuel@hostel.edu.gh');

INSERT INTO Semester
(SemesterID, AcademicYear, SemesterName, StartDate, EndDate)
VALUES
('SEM01', '2025/26', 'Semester 1', '2026-01-01', '2026-03-31'),
('SEM02', '2025/26', 'Semester 2', '2026-05-01', '2026-07-31'),
('SEM03', '2026/27', 'Semester 1', '2027-01-01', '2027-03-31'),
('SEM04', '2026/27', 'Semester 2', '2027-05-01', '2027-07-31');

INSERT INTO Student
(StudentID, FirstName, LastName, Gender, DateOfBirth, Phone, Email, Programme, Year)
VALUES
('10012028', 'John', 'Mensah', 'Male', '2005-04-12', '0234567890', 'john.mensah@ashesi.edu.gh', 'CS', 2028),
('10022027', 'Adam', 'Nortey', 'Male', '2004-09-04', '0309876543', 'adam.nortey@ashesi.edu.gh', 'BA', 2027),
('10032027', 'Abby', 'Addo', 'Female', '2004-02-05', '0234125678', 'abby.addo@ashesi.edu.gh', 'ENG', 2027),
('10042028', 'Sarah', 'Owusu', 'Female', '2005-07-18', '0245678901', 'sarah.owusu@ashesi.edu.gh', 'LLB', 2028),
('10052026', 'Michael', 'Boateng', 'Male', '2003-11-22', '0551234567', 'michael.boateng@ashesi.edu.gh', 'CS', 2026),
('10062028', 'Grace', 'Osei', 'Female', '2005-03-15', '0202345678', 'grace.osei@ashesi.edu.gh', 'BA', 2028),
('10072027', 'Daniel', 'Asare', 'Male', '2004-06-09', '0543456789', 'daniel.asare@ashesi.edu.gh', 'ENG', 2027),
('10082026', 'Linda', 'Adjei', 'Female', '2003-12-30', '0504567890', 'linda.adjei@ashesi.edu.gh', 'LLB', 2026),
('10092028', 'Samuel', 'Amoah', 'Male', '2005-01-27', '0245678012', 'samuel.amoah@ashesi.edu.gh', 'CS', 2028),
('10102027', 'Esther', 'Darko', 'Female', '2004-08-14', '0556789012', 'esther.darko@ashesi.edu.gh', 'BA', 2027),
('10112026', 'Kwame', 'Badu', 'Male', '2003-05-20', '0207890123', 'kwame.badu@ashesi.edu.gh', 'ENG', 2026),
('10122028', 'Patricia', 'Arthur', 'Female', '2005-10-11', '0548901234', 'patricia.arthur@ashesi.edu.gh', 'LLB', 2028),
('10132027', 'Joseph', 'Addo', 'Male', '2004-03-08', '0509012345', 'joseph.addo@ashesi.edu.gh', 'CS', 2027),
('10142026', 'Mary', 'Darko', 'Female', '2003-07-25', '0240123456', 'mary.darko@ashesi.edu.gh', 'BA', 2026),
('10152028', 'George', 'Tetteh', 'Male', '2005-09-16', '0551234506', 'george.tetteh@ashesi.edu.gh', 'ENG', 2028),
('10162027', 'Rebecca', 'Opoku', 'Female', '2004-11-03', '0202345617', 'rebecca.opoku@ashesi.edu.gh', 'LLB', 2027),
('10172026', 'Isaac', 'Nyarko', 'Male', '2003-04-19', '0543456728', 'isaac.nyarko@ashesi.edu.gh', 'CS', 2026),
('10182028', 'Diana', 'Quaye', 'Female', '2005-06-28', '0504567839', 'diana.quaye@ashesi.edu.gh', 'BA', 2028),
('10192027', 'Francis', 'Agyeman', 'Male', '2004-01-13', '0245678940', 'francis.agyeman@ashesi.edu.gh', 'ENG', 2027),
('10202026', 'Janet', 'Frimpong', 'Female', '2003-10-07', '0556789051', 'janet.frimpong@ashesi.edu.gh', 'LLB', 2026),
('10212028', 'Kojo', 'Annan', 'Male', '2005-02-21', '0241112233', 'kojo.annan@ashesi.edu.gh', 'CS', 2028),
('10222027', 'Yaw', 'Ofori', 'Male', '2004-05-17', '0242223344', 'yaw.ofori@ashesi.edu.gh', 'BA', 2027),
('10232026', 'Nana', 'Kumi', 'Male', '2003-08-09', '0243334455', 'nana.kumi@ashesi.edu.gh', 'ENG', 2026),
('10242028', 'Akosua', 'Baah', 'Female', '2005-01-30', '0244445566', 'akosua.baah@ashesi.edu.gh', 'CS', 2028),
('10252027', 'Esi', 'Amankwah', 'Female', '2004-12-12', '0245556677', 'esi.amankwah@ashesi.edu.gh', 'BA', 2027);

INSERT INTO Manager
(ManagerID, StaffID, AssignedHostel)
VALUES
('MF1', 'SF1', 'H1'),
('MF2', 'SF2', 'H2'),
('MF3', 'SF3', 'H3'),
('MF4', 'SF4', 'H4');

INSERT INTO Auxiliary_Staff
(AuxiliaryID, StaffID, Role)
VALUES
('ASF1', 'SF5', 'Maintenance'),
('ASF2', 'SF6', 'Security'),
('ASF3', 'SF7', 'Maintenance'),
('ASF4', 'SF8', 'Cleaner'),
('ASF5', 'SF9', 'Maintenance'),
('ASF6', 'SF10', 'Security');

INSERT INTO Block
(BlockID, BlockName, HostelID, No_of_Floors)
VALUES
('BK1', 'Araba Block', 'H1', 2),
('BK2', 'Johnson Block', 'H2', 2),
('BK3', 'Henry Block', 'H3', 2),
('BK4', 'Akua Block', 'H4', 2);

INSERT INTO Room
(RoomID, RoomNumber, Floor, Capacity, BlockID, CurrentOccupancy)
VALUES
('R1', '101', 1, 2, 'BK1', 2),
('R2', '102', 1, 2, 'BK1', 2),
('R3', '103', 1, 2, 'BK1', 2),
('R4', '104', 2, 2, 'BK1', 0),
('R5', '105', 2, 2, 'BK1', 0),
('R6', '106', 2, 2, 'BK1', 0),
('R7', '101', 1, 2, 'BK2', 2),
('R8', '102', 1, 2, 'BK2', 2),
('R9', '103', 1, 2, 'BK2', 2),
('R10', '104', 2, 2, 'BK2', 1),
('R11', '105', 2, 2, 'BK2', 0),
('R12', '106', 2, 2, 'BK2', 0),
('R13', '101', 1, 2, 'BK2', 0),
('R14', '102', 1, 2, 'BK3', 2),
('R15', '103', 1, 2, 'BK3', 2),
('R16', '104', 2, 2, 'BK3', 2),
('R17', '105', 2, 2, 'BK3', 0),
('R18', '106', 2, 2, 'BK3', 0),
('R19', '101', 1, 2, 'BK3', 0),
('R20', '102', 1, 2, 'BK4', 2),
('R21', '103', 1, 2, 'BK4', 2),
('R22', '104', 2, 2, 'BK4', 2),
('R23', '105', 2, 2, 'BK4', 0),
('R24', '106', 2, 2, 'BK4', 0),
('R25', '101', 1, 2, 'BK4', 0);

INSERT INTO Bed
(BedID, BedLabel, Status, RoomID)
VALUES
('Bed1', '1', 'Occupied', 'R1'),
('Bed2', '2', 'Occupied', 'R1'),
('Bed3', '1', 'Occupied', 'R2'),
('Bed4', '2', 'Occupied', 'R2'),
('Bed5', '1', 'Occupied', 'R3'),
('Bed6', '2', 'Occupied', 'R3'),
('Bed7', '1', 'Vacant', 'R4'),
('Bed8', '2', 'Vacant', 'R4'),
('Bed9', '1', 'Vacant', 'R5'),
('Bed10', '2', 'Vacant', 'R5'),
('Bed11', '1', 'Vacant', 'R6'),
('Bed12', '2', 'Vacant', 'R6'),
('Bed13', '1', 'Occupied', 'R7'),
('Bed14', '2', 'Occupied', 'R7'),
('Bed15', '1', 'Occupied', 'R8'),
('Bed16', '2', 'Occupied', 'R8'),
('Bed17', '1', 'Occupied', 'R9'),
('Bed18', '2', 'Occupied', 'R9'),
('Bed19', '1', 'Occupied', 'R10'),
('Bed20', '2', 'Reserved', 'R10'),
('Bed21', '1', 'Vacant', 'R11'),
('Bed22', '2', 'Vacant', 'R11'),
('Bed23', '1', 'Vacant', 'R12'),
('Bed24', '2', 'Vacant', 'R12'),
('Bed25', '1', 'Vacant', 'R13'),
('Bed26', '2', 'Vacant', 'R13'),
('Bed27', '1', 'Occupied', 'R14'),
('Bed28', '2', 'Occupied', 'R14'),
('Bed29', '1', 'Occupied', 'R15'),
('Bed30', '2', 'Occupied', 'R15'),
('Bed31', '1', 'Occupied', 'R16'),
('Bed32', '2', 'Occupied', 'R16'),
('Bed33', '1', 'Reserved', 'R17'),
('Bed34', '2', 'Reserved', 'R17'),
('Bed35', '1', 'Vacant', 'R18'),
('Bed36', '2', 'Vacant', 'R18'),
('Bed37', '1', 'Vacant', 'R19'),
('Bed38', '2', 'Vacant', 'R19'),
('Bed39', '1', 'Occupied', 'R20'),
('Bed40', '2', 'Occupied', 'R20'),
('Bed41', '1', 'Occupied', 'R21'),
('Bed42', '2', 'Occupied', 'R21'),
('Bed43', '1', 'Occupied', 'R22'),
('Bed44', '2', 'Occupied', 'R22'),
('Bed45', '1', 'Vacant', 'R23'),
('Bed46', '2', 'Vacant', 'R23'),
('Bed47', '1', 'Vacant', 'R24'),
('Bed48', '2', 'Vacant', 'R24'),
('Bed49', '1', 'Vacant', 'R25'),
('Bed50', '2', 'Vacant', 'R25');

INSERT INTO Visitor
(VisitorID, VisitorName, Phone, ApprovalStatus)
VALUES
('V1', 'David Mensah', '0241010101', 'Approved'),
('V2', 'Ama Serwaa', '0242020202', 'Approved'),
('V3', 'Kofi Owusu', '0243030303', 'Rejected'),
('V4', 'Linda Boateng', '0244040404', 'Approved'),
('V5', 'Nana Addo', '0245050505', 'Approved'),
('V6', 'Grace Quaye', '0246060606', 'Rejected'),
('V7', 'Yaw Arthur', '0247070707', 'Approved'),
('V8', 'Akua Darko', '0248080808', 'Approved'),
('V9', 'Michael Osei', '0249090909', 'Rejected'),
('V10', 'Esi Badu', '0241110000', 'Approved'),
('V11', 'Kojo Asare', '0242220000', 'Approved'),
('V12', 'Mary Adjei', '0243330000', 'Approved');

INSERT INTO Visit
(StudentID, VisitorID, CheckInTime, CheckOutTime, VisitDate)
VALUES
('10012028', 'V1', '09:00:00', '12:30:00', '2027-01-10'),
('10022027', 'V2', '10:00:00', '13:30:00', '2027-01-13'),
('10032027', 'V4', '11:00:00', '14:30:00', '2027-01-16'),
('10042028', 'V5', '12:00:00', '15:30:00', '2027-01-19'),
('10052026', 'V7', '13:00:00', '16:30:00', '2027-01-22'),
('10062028', 'V8', '09:00:00', '12:30:00', '2027-01-25'),
('10072027', 'V10', '10:00:00', '13:30:00', '2027-01-28'),
('10082026', 'V11', '11:00:00', '14:30:00', '2027-01-31'),
('10092028', 'V12', '12:00:00', '15:30:00', '2027-02-03'),
('10102027', 'V1', '13:00:00', '16:30:00', '2027-02-06'),
('10112026', 'V2', '09:00:00', '12:30:00', '2027-02-09'),
('10122028', 'V4', '10:00:00', '13:30:00', '2027-02-12'),
('10132027', 'V5', '11:00:00', '14:30:00', '2027-02-15'),
('10142026', 'V7', '12:00:00', '15:30:00', '2027-02-18'),
('10152028', 'V8', '13:00:00', '16:30:00', '2027-02-21'),
('10162027', 'V10', '09:00:00', '12:30:00', '2027-02-24'),
('10172026', 'V11', '10:00:00', '13:30:00', '2027-02-27'),
('10182028', 'V12', '11:00:00', '14:30:00', '2027-03-02'),
('10192027', 'V1', '12:00:00', '15:30:00', '2027-03-05'),
('10202026', 'V2', '13:00:00', '16:30:00', '2027-03-08');

INSERT INTO Allocation
(AllocationID, StudentID, BedID, SemesterID, AllocationStartDate, AllocationEndDate, OfferSentDate, AcceptanceDeadline, AcceptedDate, Status)
VALUES
('A00001', '10012028', 'Bed13', 'SEM02', '2026-05-01', '2026-07-31', '2026-04-01', '2026-04-08', '2026-04-03', 'Inactive'),
('A00002', '10022027', 'Bed14', 'SEM02', '2026-05-01', '2026-07-31', '2026-04-01', '2026-04-08', '2026-04-03', 'Inactive'),
('A00003', '10032027', 'Bed1', 'SEM02', '2026-05-01', '2026-07-31', '2026-04-01', '2026-04-08', '2026-04-03', 'Inactive'),
('A00004', '10042028', 'Bed2', 'SEM02', '2026-05-01', '2026-07-31', '2026-04-01', '2026-04-08', '2026-04-03', 'Inactive'),
('A00005', '10052026', 'Bed15', 'SEM02', '2026-05-01', '2026-07-31', '2026-04-01', '2026-04-08', '2026-04-03', 'Inactive'),
('A00006', '10012028', 'Bed13', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00007', '10022027', 'Bed14', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00008', '10032027', 'Bed1', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00009', '10042028', 'Bed2', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00010', '10052026', 'Bed15', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00011', '10062028', 'Bed3', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00012', '10072027', 'Bed16', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00013', '10082026', 'Bed4', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00014', '10092028', 'Bed17', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00015', '10102027', 'Bed5', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00016', '10112026', 'Bed18', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00017', '10122028', 'Bed6', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00018', '10132027', 'Bed19', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00019', '10142026', 'Bed27', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00020', '10152028', 'Bed39', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00021', '10162027', 'Bed28', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00022', '10172026', 'Bed40', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00023', '10182028', 'Bed29', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00024', '10192027', 'Bed41', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00025', '10202026', 'Bed30', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00026', '10212028', 'Bed42', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00027', '10222027', 'Bed43', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00028', '10232026', 'Bed44', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00029', '10242028', 'Bed31', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00030', '10252027', 'Bed32', 'SEM03', '2027-01-01', '2027-03-31', '2026-12-01', '2026-12-08', '2026-12-04', 'Active'),
('A00031', '10052026', 'Bed21', 'SEM04', '2027-05-01', '2027-07-31', '2027-04-01', '2027-04-08', NULL, 'Declined'),
('A00032', '10062028', 'Bed35', 'SEM04', '2027-05-01', '2027-07-31', '2027-04-01', '2027-04-08', NULL, 'Declined'),
('A00033', '10012028', 'Bed20', 'SEM04', '2027-05-01', '2027-07-31', '2027-04-10', '2027-04-17', NULL, 'Pending'),
('A00034', '10032027', 'Bed33', 'SEM04', '2027-05-01', '2027-07-31', '2027-04-10', '2027-04-17', NULL, 'Pending'),
('A00035', '10042028', 'Bed34', 'SEM04', '2027-05-01', '2027-07-31', '2027-04-10', '2027-04-17', NULL, 'Pending');

INSERT INTO Maintenance
(MaintenanceID, RoomID, StudentID, StaffID, ManagerID, IssueDescription, RequestDate, Status, DateResolved)
VALUES
('M1', 'R7', '10012028', 'SF5', 'MF2', 'Faulty tap', '2027-01-06', 'Resolved', '2027-01-09'),
('M2', 'R7', '10022027', 'SF7', 'MF2', 'Broken light', '2027-01-07', 'Pending', NULL),
('M3', 'R1', '10032027', 'SF9', 'MF1', 'Leaking pipe', '2027-01-08', 'Ok', NULL),
('M4', 'R1', '10042028', 'SF5', 'MF1', 'Blocked sink', '2027-01-09', 'Resolved', '2027-01-12'),
('M5', 'R8', '10052026', 'SF7', 'MF2', 'Damaged socket', '2027-01-10', 'Pending', NULL),
('M6', 'R2', '10062028', 'SF9', 'MF1', 'Broken chair', '2027-01-11', 'Resolved', '2027-01-14'),
('M7', 'R8', '10072027', 'SF5', 'MF2', 'Faulty fan', '2027-01-12', 'Pending', NULL),
('M8', 'R2', '10082026', 'SF7', 'MF1', 'Door lock issue', '2027-01-13', 'Ok', NULL),
('M9', 'R9', '10092028', 'SF9', 'MF2', 'Faulty tap', '2027-01-14', 'Resolved', '2027-01-17'),
('M10', 'R3', '10102027', 'SF5', 'MF1', 'Broken light', '2027-01-15', 'Pending', NULL),
('M11', 'R9', '10112026', 'SF7', 'MF2', 'Leaking pipe', '2027-01-16', 'Resolved', '2027-01-19'),
('M12', 'R3', '10122028', 'SF9', 'MF1', 'Blocked sink', '2027-01-17', 'Pending', NULL),
('M13', 'R10', '10132027', 'SF5', 'MF2', 'Damaged socket', '2027-01-18', 'Ok', NULL),
('M14', 'R14', '10142026', 'SF7', 'MF3', 'Broken chair', '2027-01-19', 'Resolved', '2027-01-22'),
('M15', 'R20', '10152028', 'SF9', 'MF4', 'Faulty fan', '2027-01-20', 'Pending', NULL),
('M16', 'R14', '10162027', 'SF5', 'MF3', 'Door lock issue', '2027-01-21', 'Resolved', '2027-01-24'),
('M17', 'R20', '10172026', 'SF7', 'MF4', 'Faulty tap', '2027-01-22', 'Pending', NULL),
('M18', 'R15', '10182028', 'SF9', 'MF3', 'Broken light', '2027-01-23', 'Ok', NULL),
('M19', 'R21', '10192027', 'SF5', 'MF4', 'Leaking pipe', '2027-01-24', 'Resolved', '2027-01-27'),
('M20', 'R15', '10202026', 'SF7', 'MF3', 'Blocked sink', '2027-01-25', 'Pending', NULL);

INSERT INTO Inspection
(InspectionID, RoomID, ManagerID, Inspection_date, RoomCondition, Remarks)
VALUES
('I1', 'R1', 'MF1', '2027-01-06', 'Good', 'Room in good condition'),
('I2', 'R2', 'MF1', '2027-01-07', 'Fair', 'Minor repairs recommended'),
('I3', 'R3', 'MF1', '2027-01-08', 'Poor', 'Maintenance attention required'),
('I4', 'R4', 'MF1', '2027-01-09', 'Good', 'Room in good condition'),
('I5', 'R5', 'MF1', '2027-01-10', 'Good', 'Room in good condition'),
('I6', 'R6', 'MF1', '2027-01-11', 'Fair', 'Minor repairs recommended'),
('I7', 'R7', 'MF2', '2027-01-12', 'Poor', 'Maintenance attention required'),
('I8', 'R8', 'MF2', '2027-01-13', 'Good', 'Room in good condition'),
('I9', 'R9', 'MF2', '2027-01-14', 'Good', 'Room in good condition'),
('I10', 'R10', 'MF2', '2027-01-15', 'Fair', 'Minor repairs recommended'),
('I11', 'R11', 'MF2', '2027-01-16', 'Poor', 'Maintenance attention required'),
('I12', 'R12', 'MF2', '2027-01-17', 'Good', 'Room in good condition'),
('I13', 'R13', 'MF2', '2027-01-18', 'Good', 'Room in good condition'),
('I14', 'R14', 'MF3', '2027-01-19', 'Fair', 'Minor repairs recommended'),
('I15', 'R15', 'MF3', '2027-01-20', 'Poor', 'Maintenance attention required'),
('I16', 'R16', 'MF3', '2027-01-21', 'Good', 'Room in good condition'),
('I17', 'R17', 'MF3', '2027-01-22', 'Good', 'Room in good condition'),
('I18', 'R18', 'MF3', '2027-01-23', 'Fair', 'Minor repairs recommended'),
('I19', 'R19', 'MF3', '2027-01-24', 'Poor', 'Maintenance attention required'),
('I20', 'R20', 'MF4', '2027-01-25', 'Good', 'Room in good condition');

INSERT INTO Payment
(PaymentID, AllocationID, StudentID, Amount_paid, Payment_Date, Payment_Method, Payment_Status, Balance_Due, Deadline)
VALUES
('P00001', 'A00001', '10012028', 1500.00, '2026-04-20', 'Bank Transfer', 'Paid', 0.00, '2026-04-30'),
('P00002', 'A00002', '10022027', 1500.00, '2026-04-20', 'Bank Transfer', 'Paid', 0.00, '2026-04-30'),
('P00003', 'A00003', '10032027', 1500.00, '2026-04-20', 'Bank Transfer', 'Paid', 0.00, '2026-04-30'),
('P00004', 'A00004', '10042028', 1500.00, '2026-04-20', 'Bank Transfer', 'Paid', 0.00, '2026-04-30'),
('P00005', 'A00005', '10052026', 1500.00, '2026-04-20', 'Bank Transfer', 'Paid', 0.00, '2026-04-30'),
('P00006', 'A00006', '10012028', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00007', 'A00006', '10012028', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00008', 'A00007', '10022027', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00009', 'A00007', '10022027', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00010', 'A00008', '10032027', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00011', 'A00008', '10032027', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00012', 'A00009', '10042028', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00013', 'A00009', '10042028', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00014', 'A00010', '10052026', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00015', 'A00010', '10052026', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00016', 'A00011', '10062028', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00017', 'A00011', '10062028', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00018', 'A00012', '10072027', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00019', 'A00012', '10072027', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00020', 'A00013', '10082026', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00021', 'A00013', '10082026', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00022', 'A00014', '10092028', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00023', 'A00014', '10092028', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00024', 'A00015', '10102027', 800.00, '2026-12-05', 'Mobile Money', 'Pending', 700.00, '2026-12-20'),
('P00025', 'A00015', '10102027', 700.00, '2026-12-12', 'Bank Transfer', 'Paid', 0.00, '2026-12-20'),
('P00026', 'A00016', '10112026', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00027', 'A00017', '10122028', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00028', 'A00018', '10132027', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00029', 'A00019', '10142026', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00030', 'A00020', '10152028', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00031', 'A00021', '10162027', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00032', 'A00022', '10172026', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00033', 'A00023', '10182028', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00034', 'A00024', '10192027', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00035', 'A00025', '10202026', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00036', 'A00026', '10212028', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00037', 'A00027', '10222027', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00038', 'A00028', '10232026', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00039', 'A00029', '10242028', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20'),
('P00040', 'A00030', '10252027', 1500.00, '2026-12-10', 'Mobile Money', 'Paid', 0.00, '2026-12-20');

INSERT INTO UserAccount
(Username, PasswordHash, Role)
VALUES
('student1', 'password', 'Student'),
('manager1', 'password', 'Manager');