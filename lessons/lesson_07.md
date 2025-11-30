# Lesson 7: OFFSET Basics

## Overview
OFFSET skips rows.

### MySQL Example
```sql
SELECT *
FROM employees
ORDER BY id
LIMIT 5 OFFSET 5;
```

### SQLite Example
```sql
SELECT *
FROM employees
ORDER BY id
LIMIT 5 OFFSET 5;
```

### Try It Yourself
Fetch rows 11–20 from employees.
