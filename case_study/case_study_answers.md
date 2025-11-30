# SQL Case Study Answers (SQLite Edition)

Below are detailed answers and explanations for all 10 case study tasks.

---

# 1. Employee Headcount by Department
```sql
SELECT d.department_name, COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.department_name
ORDER BY employee_count DESC;
```
**Explanation:**  
Counts employees grouped by department, using LEFT JOIN so departments with zero employees still appear.

---

# 2. Average Salary by Department
```sql
SELECT d.department_name, AVG(e.salary) AS avg_salary
FROM departments d
JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.department_name
ORDER BY avg_salary DESC;
```
**Explanation:**  
AVG() computes mean salary for each department.

---

# 3. Employees Hired Per Year
```sql
SELECT SUBSTR(hire_date, 1, 4) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY hire_year
ORDER BY hire_year;
```
**Explanation:**  
SQLite uses SUBSTR to extract the year from a date string.

---

# 4. Employees Missing a Department
```sql
SELECT *
FROM employees
WHERE department_id IS NULL;
```
**Explanation:**  
Finds unassigned employees; useful for data cleanup.

---

# 5. Project Staffing Levels
```sql
SELECT p.project_name, COUNT(ep.employee_id) AS num_assigned
FROM projects p
LEFT JOIN employee_projects ep ON p.id = ep.project_id
GROUP BY p.id, p.project_name
ORDER BY num_assigned DESC;
```
**Explanation:**  
LEFT JOIN ensures projects with zero staff still appear.

---

# 6. Employees Working on Multiple Projects
```sql
SELECT e.first_name, e.last_name, COUNT(ep.project_id) AS project_count
FROM employees e
JOIN employee_projects ep ON e.id = ep.employee_id
GROUP BY e.id, e.first_name, e.last_name
HAVING project_count > 1
ORDER BY project_count DESC;
```
**Explanation:**  
HAVING filters grouped rows to show only multi-project employees.

---

# 7. Employees With No Projects
```sql
SELECT *
FROM employees
WHERE id NOT IN (SELECT employee_id FROM employee_projects);
```
**Explanation:**  
NOT IN returns employees who are not assigned to any project.

---

# 8. Project Budgets by Department
```sql
SELECT d.department_name,
       SUM(p.budget) AS total_project_budget
FROM departments d
JOIN employees e ON d.id = e.department_id
JOIN employee_projects ep ON e.id = ep.employee_id
JOIN projects p ON ep.project_id = p.id
GROUP BY d.id, d.department_name
ORDER BY total_project_budget DESC;
```
**Explanation:**  
Budget is aggregated across all projects employees participate in.

---

# 9. Highest-Paid Employee Per Department
```sql
SELECT d.department_name,
       e.first_name,
       e.last_name,
       e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary = (
    SELECT MAX(salary)
    FROM employees
    WHERE department_id = e.department_id
);
```
**Explanation:**  
Subquery returns max salary per department.

---

# 10. Employees Above Company Average Salary
```sql
SELECT *
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;
```
**Explanation:**  
Compares each salary to global AVG().

