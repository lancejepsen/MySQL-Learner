# Lesson 13: LEFT JOIN

## Overview
Left join keeps all left table rows.

### MySQL Example
```sql
SELECT e.first_name, d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.id;
```

### SQLite Example
```sql
SELECT e.first_name, d.department_name
FROM employees e
LEFT JOIN departments d
ON e.department_id = d.id;
```

### Try It Yourself
List all employees even without a department match.
