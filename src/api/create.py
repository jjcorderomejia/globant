from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey, MetaData

# Define the database connection details
DB_USERNAME = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

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


# Drop the tables if they already exist
metadata.drop_all(engine)

# Create the tables in the database
metadata.create_all(engine)