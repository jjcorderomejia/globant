# Use an official Python runtime as a parent image
FROM python:3

# Create the /app directory
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt file to /app directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy migrate.py file to /app directory
COPY src/scripts/backup.py .

# Run migrate.py when the container launches
CMD ["python", "backup.py"]

