import psycopg2
import fastavro
import os
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Restore data from AVRO files to PostgreSQL tables')

# Add an argument for the table name
parser.add_argument('table', type=str, help='Name of the table to restore')

# Parse the command line arguments
args = parser.parse_args()

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


def restore_table(table_name):
    # Define the file name and path
    filename = f"{table_name}.avro"
    file_path = os.path.join(filepath, filename)

    # Read the data from the AVRO file
    with open(file_path, "rb") as f:
        avro_reader = fastavro.reader(f)
        rows = [row for row in avro_reader]

    # Convert the dictionary to a list of tuples
    rows = [tuple(row.values()) for row in rows]

    # Insert the rows into the database table
    table = tables[table_name]
    columns = [col.name for col in table.columns]
    placeholders = ','.join(['%s' for _ in columns])
    insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
    cur.executemany(insert_query, rows)
    conn.commit()
    print(f"{len(rows)} rows inserted into {table_name}")


# Call the restore_table function for each table
restore_table(args.table)

# Close the database connection
cur.close()
conn.close()
