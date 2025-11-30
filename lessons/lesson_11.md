# Lesson 11: HAVING Clause

## Overview
HAVING filters aggregated results.

### MySQL Example
```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 60000;
```

### SQLite Example
```sql
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 60000;
```

### Try It Yourself
Show departments with more than 5 employees.
