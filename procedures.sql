DELIMITER //

CREATE PROCEDURE sp_AllocateBed(
    IN p_AllocationID VARCHAR(6),
    IN p_StudentID VARCHAR(8),
    IN p_BedID VARCHAR(10),
    IN p_SemesterID VARCHAR(10),
    IN p_StartDate DATE,
    IN p_EndDate DATE
)
BEGIN

    DECLARE v_BedStatus VARCHAR(20);
    DECLARE v_ExistingAllocation INT DEFAULT 0;


    SELECT Status
    INTO v_BedStatus
    FROM Bed
    WHERE BedID = p_BedID;


    IF v_BedStatus IS NULL THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bed does not exist';

    ELSEIF v_BedStatus <> 'Vacant' THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bed is not available';

    END IF;


    SELECT COUNT(*)
    INTO v_ExistingAllocation
    FROM Allocation
    WHERE StudentID = p_StudentID
      AND Status = 'Active';


    IF v_ExistingAllocation > 0 THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Student already has an active allocation';

    END IF;


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
        p_AllocationID,
        p_StudentID,
        p_BedID,
        p_SemesterID,
        p_StartDate,
        p_EndDate,
        CURDATE(),
        DATE_ADD(CURDATE(), INTERVAL 7 DAY),
        CURDATE(),
        'Active'
    );

END //

DELIMITER ;




DELIMITER //

CREATE PROCEDURE sp_ProcessPayment(
    IN p_PaymentID VARCHAR(10),
    IN p_AllocationID VARCHAR(6),
    IN p_StudentID VARCHAR(8),
    IN p_Amount DECIMAL(10,2),
    IN p_PaymentMethod VARCHAR(20),
    IN p_TotalAmount DECIMAL(10,2),
    IN p_Deadline DATE
)
BEGIN

    DECLARE v_Balance DECIMAL(10,2);


    IF p_Amount <= 0 THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Payment amount must be greater than zero';

    END IF;


    IF p_Amount > p_TotalAmount THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Payment cannot exceed the total amount due';

    END IF;


    SET v_Balance =
        p_TotalAmount - p_Amount;


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
    VALUES
    (
        p_PaymentID,
        p_AllocationID,
        p_StudentID,
        p_Amount,
        CURDATE(),
        p_PaymentMethod,

        CASE
            WHEN v_Balance = 0
            THEN 'Paid'

            ELSE 'Pending'
        END,

        v_Balance,
        p_Deadline
    );

END //

DELIMITER ;






DELIMITER //

CREATE PROCEDURE sp_StudentAllocationReport(
    IN p_StudentID VARCHAR(8)
)
BEGIN

    SELECT
        s.StudentID,
        CONCAT(
            s.FirstName,
            ' ',
            s.LastName
        ) AS StudentName,
        s.Programme,
        s.Year,
        h.HostelName,
        b.BlockName,
        r.RoomNumber,
        bed.BedLabel,
        sem.AcademicYear,
        sem.SemesterName,
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

    JOIN Semester sem
        ON a.SemesterID = sem.SemesterID

    WHERE
        s.StudentID = p_StudentID

    ORDER BY
        a.AllocationStartDate DESC;

END //

DELIMITER ;

