# Lesson 14: RIGHT JOIN (SQLite Workaround)

## SQLite Note
SQLite does NOT support RIGHT JOIN.

### Convert RIGHT JOIN to LEFT JOIN

#### MySQL
```sql
SELECT *
FROM employees e
RIGHT JOIN departments d
ON e.department_id = d.id;
```

#### SQLite Equivalent
```sql
SELECT *
FROM departments d
LEFT JOIN employees e
ON e.department_id = d.id;
```

### Try It Yourself
Rewrite a RIGHT JOIN as a LEFT JOIN.
