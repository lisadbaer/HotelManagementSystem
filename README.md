Project Name: Hostel Management System

Memebers:
Khadijah Mahrouf Yusif | 43692028 
Fredda Nyarko | 92602028 
Lisa Baer | 47592028 
Kendise Quartey | 40432028 
Chol Maguet Thiong | 51632027 



Technologies used:
Python – Used to implement the application logic.
Streamlit – Used to create the web application and user interface.
MariaDB – Used as the relational database management system.
SQL – Used for database creation, data manipulation, queries, views, procedures, functions, triggers, and access control.
MariaDB Python Connector – Used to connect the Python application to the MariaDB database.
Git/GitHub – Used for version control and collaboration.



Database management system used:
MariaDB – Used as the Database Management System (DBMS) to create, store, manage, and retrieve data for the University Hostel Management System.



Programming language:
Python – Used to develop the web application, implement the application logic, and connect the Streamlit interface to the MariaDB database.



How to install the application:
1) Clone or download the project
git clone <repository-link>
cd <project-folder>

2) Install the required Python packages
python -m pip install streamlit mariadb

3) Install MariaDB and start the MariaDB server.

4) Create the database by running the provided SQL script in MariaDB.

5) Configure the database connection in database.py with the correct database name, username, and password.

6) Run the application
python -m streamlit run app.py
The application will open in your web browser.




How to create the database:

1) Open MariaDB and log in:
mariadb -u root -p

2) Create the database:
CREATE DATABASE Hostel_Management;

3) Select the database:
USE Hostel_Management;

4) Run the provided SQL script to create the tables, constraints, and populate the database:
SOURCE path/to/hostel_management.sql;

For example:
SOURCE C:/Users/YourName/Documents/hostel_management.sql;

5) Confirm that the tables were created:
SHOW TABLES;




How to populate the database:

1) Make sure the database has been created and selected:
USE Hostel_Management;

2) Run the provided SQL file:
SOURCE path/to/hostel_management.sql;

3) Verify that data was inserted by running:
SELECT * FROM Student;
SELECT * FROM Hostel;
SELECT * FROM Room;




How to run the application:

1) Open a terminal in the project folder.

2) Make sure the MariaDB server is running and the Hostel_Management database has been created and populated.

3) Make sure the database credentials in database.py are correct.

4) Start the Streamlit application:
python -m streamlit run app.py

The application should automatically open in your web browser. If it does not, copy the Local URL displayed in the terminal and open it in your browser.



