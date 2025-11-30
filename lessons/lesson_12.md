# Lesson 12: INNER JOIN

## Overview
Combines rows from two tables.

### MySQL Example
```sql
SELECT e.first_name, d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.id;
```

### SQLite Example
```sql
SELECT e.first_name, d.department_name
FROM employees e
INNER JOIN departments d
ON e.department_id = d.id;
```

### Try It Yourself
Join employees with their departments.
