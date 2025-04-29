create database dbms;
CREATE TABLE Department (
    Department_ID INT PRIMARY KEY AUTO_INCREMENT,
    Department_Name VARCHAR(100) NOT NULL,
    Department_Type VARCHAR(100),
    Contact_Info VARCHAR(150),
    Resources VARCHAR(200), 
    Tasks VARCHAR(200) 
);
describe Department;
CREATE TABLE Employee (
    Employee_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(100) NOT NULL,
    Last_Name VARCHAR(100) NOT NULL,
    Designation VARCHAR(100),
    Contact_Info VARCHAR(150),
    Department_ID INT NOT NULL,
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);
CREATE TABLE Employee_Project (
    Employee_ID INT NOT NULL,
    Project_ID INT NOT NULL,
    PRIMARY KEY (Employee_ID, Project_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);
CREATE TABLE Discussion_Forum (
    Discussion_ID INT PRIMARY KEY AUTO_INCREMENT,
    Discussion_Type VARCHAR(100),
    Conclusion VARCHAR(200),
    Date_Created DATE,
    Project_ID INT NOT NULL,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID)
);
describe Discussion_Forum;
desc Project;
INSERT INTO Department (Department_ID, Department_Name, Department_Type, Contact_Info, Resources, Tasks) 
VALUES 
(1, 'IT', 'Technology', 'it@company.com', 'Computers, Servers', 'Software Development'),
(2, 'HR', 'Human Resources', 'hr@company.com', 'Employee Records', 'Hiring, Training'),
(3, 'Finance', 'Accounts', 'finance@company.com', 'Financial Reports', 'Budgeting'),
(4, 'Marketing', 'Business', 'marketing@company.com', 'Ad Campaigns', 'Market Research'),
(5, 'Operations', 'Logistics', 'operations@company.com', 'Supply Chain', 'Inventory Management');
INSERT INTO Employee (Employee_ID, First_Name, Last_Name, Designation, Contact_Info, Department_ID) 
VALUES 
(1, 'Harry', 'Potter', 'Software Engineer', 'harry@company.com', 1),
(2, 'Hermoine', 'Granger', 'HR Manager', 'hermoine@company.com', 2),
(3, 'Ron', 'Weasley', 'Finance Analyst', 'ron@company.com', 3),
(4, 'Draco', 'Malfoy', 'Marketing Lead', 'draco@company.com', 4),
(5, 'Sirius', 'Black', 'Operations Manager', 'sirius@company.com', 5);
INSERT INTO Project (Project_ID, Project_Name, Location, Start_Date, End_Date, Department_ID) 
VALUES 
(1, 'AI Development', 'Hyderabad', '2025-01-01', '2025-12-31', 1),
(2, 'Employee Wellness', 'Bengaluru', '2025-02-15', '2025-09-30', 2),
(3, 'Budget Planning 2025', 'Chennai', '2025-03-01', '2025-11-30', 3),
(4, 'Ad Campaign 2024', 'Mumbai', '2025-04-10', '2025-12-15', 4),
(5, 'Warehouse Automation', 'New Delhi', '2025-05-20', '2025-10-10', 5);
INSERT INTO Employee_Project (Employee_ID, Project_ID) 
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
INSERT INTO Discussion_Forum (Discussion_ID, Discussion_Type, Conclusion, Date_Created, Project_ID) 
VALUES 
(1, 'Technical', 'Adopt Python for AI', '2025-01-15', 1),
(2, 'HR Policies', 'Increase employee benefits', '2025-02-20', 2),
(3, 'Finance Review', 'Cut unnecessary expenses', '2025-03-05', 3),
(4, 'Marketing Strategies', 'Focus on social media', '2025-04-25', 4),
(5, 'Logistics Optimization', 'Use AI-driven solutions', '2025-06-01', 5);
Select * from employee;
select * from Project;
Select * from employee_project;
select * from discussion_forum;
ALTER TABLE Project ADD COLUMN Status VARCHAR(255);
ALTER TABLE Project ADD COLUMN Proof VARCHAR(255);
INSERT INTO Department (Department_ID,Department_Name, Department_Type, Contact_Info, Resources, Tasks)
VALUES (6,'admin', 'Superuser', 'admin@gmail.com', 'All Access', 'Oversee All Projects');
ALTER TABLE Project ADD COLUMN Assigned BOOLEAN DEFAULT TRUE;
UPDATE Project SET Assigned = FALSE WHERE Department_ID IS NULL;
ALTER TABLE Project MODIFY COLUMN Department_ID INT NULL;
CREATE TABLE Chat (
    Chat_ID INT AUTO_INCREMENT PRIMARY KEY,
    Sender_Department VARCHAR(100),
    Receiver_Department VARCHAR(100),
    Message TEXT NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


