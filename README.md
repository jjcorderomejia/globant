# Employee Data Migration

This script migrates employee data from CSV files to a PostgreSQL database. It uses Flask as a web framework and SQLAlchemy as an ORM.

## Setup

1. Clone this repository: `git clone https://github.com/jjcorderomejia/globant.git`
2. Install the required Python packages: `pip install -r requirements.txt`
3. Set up the database connection details in `migrate2.py` file (`DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`)
4. Initialize your local project as a Git repository by running `git init` in the root directory of your project.
5. Run the Flask app: `python migrate2.py`
6. Run the python file src/api/create.py for creating the  tables: departments, jobs and hired_employees
7. Send a POST request to `http://localhost:5000/parse-csv` to migrate the data from CSV files to the database.
8. Used a virtual environment for this project: need to execute these lines  python3.8 -m venv globant-venv    source globant-venv/bin/activate  (optional) you can use your own environment.

## Instuctions

### Challenge 1

For these requirements "Move historic data from files in CSV format to the new database." and "Create a Rest API service to receive new data."  execute `python src/api/migrate3.py` and then `curl -X POST -u admin:password http://localhost:5000/parse-csv` on command line.

For this requirement "Create a feature to backup for each table and save it in the file system in AVRO format." execute `python src/scripts/backup.py`

For this requirement "Create a feature to restore a certain table with its backup" execute `python src/scripts/restore2.py`

### Challenge 2

For this requirement: "Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job" execute `python src/api/reports` and then on a web browser `http://localhost:5000/employee_count` use this credentials when asked:  user: 'admin', password: 'password'.

For this requirement: "List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending)." execute `python src/api/reports` and then on a web browser `http://localhost:5000/hiring` use this credentials when asked:  user: 'admin', password: 

For this requirement "Create a visual report for each requirement using your favorite tool" execute `python src/api/reports` and then on a web browser `http://localhost:5000/hiring_graph` use this credentials when asked:  user: 'admin', password: 
 
## CSV Files

This script uses the following CSV files:

- `/home/jjcm/Projects/globant/data/departments.csv`
- `/home/jjcm/Projects/globant/data/jobs.csv`
- `/home/jjcm/Projects/globant/data/hired_employees.csv`

## Database Tables

This script creates the following tables in the database:

### departments

| Column         | Type    |
|----------------|---------|
| id             | integer |
| department     | string  |

### jobs

| Column         | Type    |
|----------------|---------|
| id             | integer |
| job            | string  |

### hired_employees

| Column         | Type     |
|----------------|----------|
| id             | integer  |
| name           | string   |
| datetime       | datetime |
| department_id  | integer  |
| job_id         | integer  |

## Error Logging

If any rows are missing or incomplete in the CSV files, the script logs the missing rows to `/home/jjcm/Projects/globant/src/err/missing_rows.log`.
