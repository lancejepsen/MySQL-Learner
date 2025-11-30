# Lesson 20: Basic Subqueries

## Overview
Subqueries run inside another query.

### SQLite Example
```sql
SELECT first_name
FROM employees
WHERE salary >
      (SELECT AVG(salary) FROM employees);
```

### Try It Yourself
Find employees above average salary.
