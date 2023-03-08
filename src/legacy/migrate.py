import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey, MetaData

# Define the database connection details
DB_USERNAME = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

# Define the CSV file paths
DEPARTMENTS_CSV = '/home/jjcm/Projects/globant/data/departments.csv'
JOBS_CSV = '/home/jjcm/Projects/globant/data/jobs.csv'
HIRED_EMPLOYEES_CSV = '/home/jjcm/Projects/globant/data/hired_employees.csv'
LOG_ERR = '/home/jjcm/Projects/globant/src/err/'

# Define the data dictionary for each table
DEPARTMENTS_DATA_DICT = {
    'id': int,
    'department': str
}
JOBS_DATA_DICT = {
    'id': int,
    'job': str
}
HIRED_EMPLOYEES_DATA_DICT = {
    'id': int,
    'name': str,
    'datetime': str,
    'department_id': int,
    'job_id': int
}

# Define the SQLAlchemy engine
engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Define the metadata
metadata = MetaData()

# Define the tables
departments = Table(
    'departments', metadata,
    Column('id', Integer),
    Column('department', String)
)

jobs = Table(
    'jobs', metadata,
    Column('id', Integer),
    Column('job', String)
)

hired_employees = Table(
    'hired_employees', metadata,
    Column('id', Integer),
    Column('name', String),
    Column('datetime', DateTime),
    Column('department_id', Integer),
    Column('job_id', Integer)
)


# Define a function to parse CSV files and return a list of dicts
def parse_csv_file(file_path, data_dict):
    missing_rows = []
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != len(data_dict):
                missing_rows.append(row)
            else:
                if all(row):
                    yield {k: data_dict[k](v) for k, v in zip(data_dict.keys(), row)}
                else:
                    missing_rows.append(row)
    # print(missing_rows)
    if missing_rows:
        with open(f'{LOG_ERR}missing_rows.log', 'a') as f:
            f.write(f'Missing rows in file: {file_path}\n')
            for row in missing_rows:
                f.write(f'Row {reader.line_num}: {row}\n')
            print(f'Inserted {len(missing_rows)} rows into {LOG_ERR}missing_rows.log error file')


# Define a function to insert data in batches
def insert_in_batches(table, data_list, batch_size):
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        conn.execute(table.insert().values(batch))
        conn.commit()
        print(f'Inserted {len(batch)} rows into {table.name} table')


# Parse the CSV files and insert the data into the database
with engine.connect() as conn:
    departments_data = list(parse_csv_file(DEPARTMENTS_CSV, DEPARTMENTS_DATA_DICT))
    insert_in_batches(departments, departments_data, 1000)

    jobs_data = list(parse_csv_file(JOBS_CSV, JOBS_DATA_DICT))
    insert_in_batches(jobs, jobs_data, 1000)

    hired_employees_data = list(parse_csv_file(HIRED_EMPLOYEES_CSV, HIRED_EMPLOYEES_DATA_DICT))
    insert_in_batches(hired_employees, hired_employees_data, 1000)



