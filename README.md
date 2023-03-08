Employee Data Migration
This script migrates employee data from CSV files to a PostgreSQL database. It uses Flask as a web framework and SQLAlchemy as an ORM.

Setup
Clone this repository: git clone https://github.com/jjcorderomejia/globant.git
Install the required Python packages: pip install -r requirements.txt
Set up the database connection details in migrate2.py file (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
Initialize your local project as a Git repository by running git init in the root directory of your project.
Run the Flask app: python migrate2.py
Send a POST request to http://localhost:5000/parse-csv to migrate the data from CSV files to the database.
CSV Files
This script uses the following CSV files:

/home/jjcm/Projects/globant/data/departments.csv
/home/jjcm/Projects/globant/data/jobs.csv
/home/jjcm/Projects/globant/data/hired_employees.csv
Database Tables
This script creates the following tables in the database:

departments
Column	Type
id	integer
department	string
jobs
Column	Type
id	integer
job	string
hired_employees
Column	Type
id	integer
name	string
datetime	datetime
department_id	integer
job_id	integer
Error Logging
If any rows are missing or incomplete in the CSV files, the script logs the missing rows to /home/jjcm/Projects/globant/src/err/missing_rows.log.
