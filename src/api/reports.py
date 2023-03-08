import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# Define the database connection details
DB_USERNAME = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'


@app.route('/employee_count', methods=['GET'])
def employee_count():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    query = '''
    SELECT 
        departments.department department,
        jobs.job job,
        COUNT(CASE 
            WHEN EXTRACT(MONTH FROM datetime) BETWEEN 1 AND 3 
            THEN hired_employees.id 
            ELSE NULL 
        END) AS q1_count,
        COUNT(CASE 
            WHEN EXTRACT(MONTH FROM datetime) BETWEEN 4 AND 6 
            THEN hired_employees.id 
            ELSE NULL 
        END) AS q2_count,
        COUNT(CASE 
            WHEN EXTRACT(MONTH FROM datetime) BETWEEN 7 AND 9 
            THEN hired_employees.id 
            ELSE NULL 
        END) AS q3_count,
        COUNT(CASE 
            WHEN EXTRACT(MONTH FROM datetime) BETWEEN 10 AND 12 
            THEN hired_employees.id 
            ELSE NULL 
        END) AS q4_count
    FROM 
        departments 
    INNER JOIN 
        hired_employees ON departments.id = hired_employees.department_id 
    INNER JOIN 
        jobs ON jobs.id = hired_employees.job_id 
    WHERE 
        EXTRACT(YEAR FROM datetime) = 2021 
    GROUP BY 
        departments.department, jobs.job 
    ORDER BY 
        departments.department, jobs.job
    '''
    cur.execute(query)
    result = cur.fetchall()
    table = "| Department | Job | Q1 | Q2 | Q3 | Q4 |\n| --- | --- | --- | --- | --- | --- |\n"
    for row in result:
        table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |\n"
    cur.close()
    conn.close()
    return table, 200


@app.route('/hiring', methods=['GET'])
def hiring():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    query = """
    SELECT d.id, d.department, COUNT(*) AS hired
    FROM hired_employees he
    JOIN departments d ON d.id = he.department_id
    WHERE DATE_TRUNC('year', he.datetime) = '2021-01-01'
    GROUP BY d.id, d.department
    HAVING COUNT(*) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM hired_employees GROUP BY department_id) AS sub)
    ORDER BY hired DESC;
    """
    cur.execute(query)
    result = cur.fetchall()
    response = []
    for row in result:
        response.append({'id': row[0], 'department': row[1], 'hired': row[2]})
    cur.close()
    conn.close()
    return response, 200



if __name__ == '__main__':
    app.run()
