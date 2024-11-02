Al Madina Academy
Overview
Al Madina Academy is a web application designed for managing attendance and courses for students. Built using HTML, CSS, JavaScript, Flask, and MySQL, this application provides an intuitive interface for both students and administrators.

Technologies Used
Frontend: HTML, CSS, JavaScript (Bootstrap for styling)
Backend: Flask (Python framework)
Database: MySQL
Other: Jinja2 (for templating), Font Awesome (for icons)
Features
Admin Dashboard: Manage courses, students, and attendance.
Mark Attendance: Ability to mark students as present or absent for specific courses.
Attendance Report: View attendance reports by course.
User Management: Admin can manage users.
Getting Started
Prerequisites
Before you begin, ensure you have the following installed:

Python (version 3.x)
MySQL Server
Flask (Install via pip)
Flask-MySQLdb (Install via pip)
Installation
Clone the Repository

Download or clone the project files from your source.
Set Up MySQL Database

Create a MySQL database for the application:
sql
Copy code
CREATE DATABASE al_madina_academy;
Use the provided SQL scripts to create the necessary tables:
Courses
Students
Attendance
Configure Flask Application

Navigate to the directory of your project.
Set up a virtual environment:
bash
Copy code
python -m venv venv
Activate the virtual environment:
On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install Flask and required packages:
bash
Copy code
pip install Flask Flask-MySQLdb
Update Configuration

In your Flask application file (e.g., app.py), configure the database connection:
python
Copy code
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'al_madina_academy'
Run the Application

Start your Flask application:
bash
Copy code
python app.py
Open your web browser and navigate to http://127.0.0.1:5000.
Directory Structure
bash
Copy code
/al_madina_academy
    /static
        /css
        /js
    /templates
        /admin
        /user
    app.py
    requirements.txt
Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

License
This project is licensed under the MIT License.

Additionally

cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
ENTER PASSWORD:

To change pswd
USE mysql;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
