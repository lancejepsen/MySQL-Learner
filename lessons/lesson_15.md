# Lesson 15: UNION Basics

## Overview
Combine results from multiple SELECTs.

### MySQL Example
```sql
SELECT first_name FROM employees
UNION
SELECT project_name FROM projects;
```

### SQLite Example
```sql
SELECT first_name FROM employees
UNION
SELECT project_name FROM projects;
```

### Try It Yourself
Combine two different name lists.
