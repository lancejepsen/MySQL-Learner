# Lesson 10: GROUP BY Basics

## Overview
GROUP BY organizes rows for aggregation.

### MySQL Example
```sql
SELECT department_id, COUNT(*) AS staff_count
FROM employees
GROUP BY department_id;
```

### SQLite Example
```sql
SELECT department_id, COUNT(*) AS staff_count
FROM employees
GROUP BY department_id;
```

### Try It Yourself
Show average salary per department.
