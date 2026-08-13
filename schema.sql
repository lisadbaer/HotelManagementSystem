ALTER TABLE Student
ADD UserID INT UNIQUE,
ADD FOREIGN KEY (UserID)
REFERENCES UserAccount(UserID);

ALTER TABLE Manager
ADD UserID INT UNIQUE,
ADD FOREIGN KEY (UserID)
REFERENCES UserAccount(UserID);

INSERT INTO UserAccount
(Username, PasswordHash, Role)
VALUES
('student1', 'TEMP_PASSWORD', 'Student'),
('manager1', 'TEMP_PASSWORD', 'Manager');