# Al-Madina Project

Al-Madina is a web application developed to manage various aspects of a student and course management system, along with attendance tracking. It provides an intuitive interface for admins to manage students, courses, and attendance while offering students a personalized dashboard to track their academic progress.

## Features

- **Admin Dashboard**: Manage student data, view courses, and track attendance.
- **Student Dashboard**: View personalized course information, attendance records, and more.
- **Attendance Management**: Record and view attendance for students in different courses.
- **Responsive Design**: The website is fully responsive and works on various screen sizes, making it accessible on all devices.
- **Admin and User Role**: Differentiates between admin and user roles for appropriate access and controls.

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap (for responsive design)
  
- **Backend**:
  - Flask (Python framework)
  - MySQL (for database management)

- **Others**:
  - jQuery (for interactive elements)
  - Git (version control)

## Setup and Installation

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)
- MySQL (or access to a MySQL server)

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/MubbassirKhan/Al-Madina.git
cd Al-Madina


Install Dependencies
Create a virtual environment and install the necessary Python packages:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
Setup MySQL Database
Make sure MySQL is installed and running. Then, create the necessary database and tables.

Create a new database in MySQL:
sql
Copy
Edit
CREATE DATABASE al_madina;
Create the necessary tables (students, courses, attendance, etc.) by using the SQL schema provided in the project or from the application logic.
Running the Flask Application
To run the app locally, use the following command:

bash
Copy
Edit
python app.py
The application will run on http://127.0.0.1:5000/ by default.

Configuring Environment Variables
Ensure your application has the correct database configurations. You can use a .env file or configure the settings directly in your Flask app, like so:

python
Copy
Edit
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_user'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'al_madina'
Contributing
We welcome contributions! If you'd like to contribute to the project, feel free to fork the repository, make changes, and create a pull request.

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Push to your forked repository.
Create a pull request with a description of your changes.
