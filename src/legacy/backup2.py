import psycopg2
import fastavro
import os

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

# Define the tables to backup
tables = ['departments', 'jobs', 'hired_employees']

# Define the file path
filepath = "/home/jjcm/Projects/globant/backup"

# Iterate over the tables and backup data to AVRO files
for table_name in tables:
    # Fetch all rows from the table
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    # Convert rows to a list of dictionaries
    rows2 = []
    for row in rows:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col] = row[i]
        rows2.append(row_dict)

    # Define the file name and path
    filename = f"{table_name}.avro"
    file_path = os.path.join(filepath, filename)

    # Write the data to the AVRO file
    with open(file_path, "wb") as f:
        fastavro.writer(f, schemas[table_name], rows2)

# Close the database connection
cur.close()
conn.close()
