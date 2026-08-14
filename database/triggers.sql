DELIMITER //

CREATE TRIGGER trg_PreventOccupiedBedAllocation
BEFORE INSERT ON Allocation
FOR EACH ROW

BEGIN

    DECLARE v_Status VARCHAR(20);


    IF NEW.Status = 'Active' THEN

        SELECT Status
        INTO v_Status
        FROM Bed
        WHERE BedID = NEW.BedID;


        IF v_Status IS NULL THEN

            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
            'Business Rule Violation: Bed does not exist.';


        ELSEIF v_Status <> 'Vacant' THEN

            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
            'Business Rule Violation: Bed is not available.';

        END IF;

    END IF;

END //

DELIMITER ;



DELIMITER //

CREATE TRIGGER trg_UpdateBedAfterAllocation
AFTER INSERT ON Allocation
FOR EACH ROW

BEGIN

    DECLARE v_RoomID VARCHAR(10);


    IF NEW.Status = 'Active' THEN

        SELECT RoomID
        INTO v_RoomID
        FROM Bed
        WHERE BedID = NEW.BedID;


        UPDATE Bed
        SET Status = 'Occupied'
        WHERE BedID = NEW.BedID;


        UPDATE Room
        SET CurrentOccupancy =
            CurrentOccupancy + 1
        WHERE RoomID = v_RoomID;

    END IF;

END //

DELIMITER ;





DELIMITER //

CREATE TRIGGER trg_PreventRoomOverCapacity
BEFORE UPDATE ON Bed
FOR EACH ROW

BEGIN

    DECLARE v_Capacity INT;
    DECLARE v_Occupancy INT;


    IF NEW.Status = 'Occupied'
       AND OLD.Status <> 'Occupied' THEN


        SELECT
            Capacity,
            CurrentOccupancy

        INTO
            v_Capacity,
            v_Occupancy

        FROM Room

        WHERE
            RoomID = NEW.RoomID;


        IF v_Occupancy >= v_Capacity THEN

            SIGNAL SQLSTATE '45000'

            SET MESSAGE_TEXT =
            'Business Rule Violation: Room capacity cannot be exceeded.';

        END IF;

    END IF;

END //

DELIMITER ;



