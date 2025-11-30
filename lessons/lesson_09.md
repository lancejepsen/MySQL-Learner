# Lesson 9: SUM, AVG, MIN, MAX

## Overview
Aggregate numeric columns.

### MySQL Example
```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;
```

### SQLite Example
```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;
```

### Try It Yourself
Find highest salary in the company.
