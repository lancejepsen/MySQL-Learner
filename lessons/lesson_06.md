# Lesson 6: LIMIT & Pagination

## Overview
LIMIT restricts returned rows.

### MySQL Example
```sql
SELECT *
FROM employees
ORDER BY hire_date DESC
LIMIT 5;
```

### SQLite Example
```sql
SELECT *
FROM employees
ORDER BY hire_date DESC
LIMIT 5;
```

### Try It Yourself
Return only the first 3 employees alphabetically.
