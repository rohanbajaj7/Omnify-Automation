Automated Employee Management Test
This repository contains a Selenium + Pytest automation script that logs into an HR management system, adds employees, verifies them, deletes them, and logs out.

Features
1.Logs in using Admin credentials.
2.Adds three new employees with unique IDs and login credentials.
3.Verifies the employees exist in the list (handles scrolling and pagination).
4.Deletes the employees after verification.
5.Logs out safely from the system.

How It Works
1.Login
Uses username: Admin and password: admin123
Waits for the dashboard to fully load before performing actions.

2.Add Employees
Fills in employee personal and login details.
Waits for page loaders to disappear before interacting with forms.

3.Verify Employees
Scrolls through the employee list and navigates pagination to find added employees.
Prints a report if any employee is not found.

4.Delete Employees
Searches for each employee by ID and deletes them one by one.
Confirms deletion and waits for loaders to disappear.

5.Logout
Clicks the profile picture to open the dropdown and logs out.
Waits for the login page to appear.

Installation & Running the Test
git clone <repository_url>
cd <repository_name>
pip install -r requirements.txt
pytest -v
