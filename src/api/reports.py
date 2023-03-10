# reports.py
import os
import psycopg2
from flask import Flask, render_template
import json
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

# Define the database connection details
DB_USERNAME = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'


@app.route('/employee_count', methods=['GET'])
@basic_auth.required
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
    cur.close()
    conn.close()

    table = "<table><thead><tr><th>Department</th><th>Job</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th></tr></thead><tbody>"

    for row in result:
        table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"

    table += "</tbody></table>"

    return table, 200


@app.route('/hiring', methods=['GET'])
@basic_auth.required
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

    table = "<table><thead><tr><th>Department ID</th><th>Department</th><th>Number of Hires</th></tr></thead><tbody>"
    for row in result:
        table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    table += "</tbody></table>"

    cur.close()
    conn.close()
    return table, 200


@app.route('/hiring_graph', methods=['GET'])
@basic_auth.required
def hiring_graph():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    query = """
    SELECT d.department, COUNT(*) AS hired
    FROM hired_employees he
    JOIN departments d ON d.id = he.department_id
    WHERE DATE_TRUNC('year', he.datetime) = '2021-01-01'
    GROUP BY d.department
    HAVING COUNT(*) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM hired_employees GROUP BY department_id) AS sub)
    ORDER BY hired DESC;
    """
    cur.execute(query)
    result = cur.fetchall()

    data = {"departments": [], "hires": []}
    for row in result:
        data["departments"].append(row[0])
        data["hires"].append(row[1])
    chart_data = json.dumps(data)

    cur.close()
    conn.close()

    return render_template('hiring_graph.html', chart_data=chart_data)


if __name__ == '__main__':
    app.run()
