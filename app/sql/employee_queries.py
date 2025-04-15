def get_employees_per_quarter_query(year: int) -> str:
    return f"""
    SELECT d.department, j.job,
        SUM(CASE WHEN strftime('%Y-%m', he.datetime) = '{year}-01' OR strftime('%Y-%m', he.datetime) = '{year}-02' OR strftime('%Y-%m', he.datetime) = '{year}-03' THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN strftime('%Y-%m', he.datetime) = '{year}-04' OR strftime('%Y-%m', he.datetime) = '{year}-05' OR strftime('%Y-%m', he.datetime) = '{year}-06' THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN strftime('%Y-%m', he.datetime) = '{year}-07' OR strftime('%Y-%m', he.datetime) = '{year}-08' OR strftime('%Y-%m', he.datetime) = '{year}-09' THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN strftime('%Y-%m', he.datetime) = '{year}-10' OR strftime('%Y-%m', he.datetime) = '{year}-11' OR strftime('%Y-%m', he.datetime) = '{year}-12' THEN 1 ELSE 0 END) AS Q4
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
    WHERE strftime('%Y', he.datetime) = '{year}'
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """
def get_departments_above_average(year: int) -> str:
    return f"""
    SELECT d.id, d.department, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE strftime('%Y', he.datetime) = '{year}'
    GROUP BY d.id, d.department
    HAVING COUNT(*) > (
        SELECT AVG(hired_count)
        FROM (
            SELECT COUNT(*) as hired_count
            FROM hired_employees
            WHERE strftime('%Y', datetime) = '{year}'
            GROUP BY department_id
        )
    )
    ORDER BY hired DESC
    """