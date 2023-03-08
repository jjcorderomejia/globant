import psycopg2
import fastavro
import os
from argparse import ArgumentParser
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

# Define the schemas for the AVRO files
schemas = {
    'departments': {
        "type": "record",
        "name": "departments",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "department", "type": "string"}
        ]
    },
    'jobs': {
        "type": "record",
        "name": "jobs",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "job", "type": "string"}
        ]
    },
    'hired_employees': {
        "type": "record",
        "name": "hired_employees",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"},
            {"name": "datetime", "type": {"type": "long", "logicalType": "timestamp-millis"}},
            {"name": "department_id", "type": "int"},
            {"name": "job_id", "type": "int"}
        ]
    }
}

# Define the database connection details
DB_USERNAME = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Define the tables
metadata = MetaData()
tables = {
    'departments': Table('departments', metadata,
                         Column('id', Integer),
                         Column('department', String)
                         ),
    'jobs': Table('jobs', metadata,
                  Column('id', Integer),
                  Column('job', String)
                  ),
    'hired_employees': Table('hired_employees', metadata,
                             Column('id', Integer),
                             Column('name', String),
                             Column('datetime', DateTime),
                             Column('department_id', Integer),
                             Column('job_id', Integer)
                             )
}

# Define the file path
filepath = "/home/jjcm/Projects/globant/backup"

# Parse command line arguments
parser = ArgumentParser()
parser.add_argument("table", help="Name of the table to restore")
args = parser.parse_args()

# Check that the specified table is valid
if args.table not in tables:
    print(f"Error: Invalid table name '{args.table}'")
    exit(1)

# Truncate the table before restoring
cur.execute(f"TRUNCATE TABLE {args.table}")

# Open the AVRO file and restore data to the table
filename = f"{args.table}.avro"
file_path = os.path.join(filepath, filename)
with open(file_path, "rb") as f:
    cur.copy_expert(f"COPY {args.table} FROM STDIN WITH (FORMAT 'binary')", f)

# Commit the changes and close the database connection
conn.commit()
cur.close()
conn.close()
