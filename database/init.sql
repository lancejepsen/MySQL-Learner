PRAGMA foreign_keys = ON;

---------------------------------------------------------
-- DROP TABLES (safe resets for SQLite)
---------------------------------------------------------
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS projects;

---------------------------------------------------------
-- TABLE: departments
---------------------------------------------------------
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
);

INSERT INTO departments (id, department_name) VALUES
(1, 'Human Resources'),
(2, 'Information Technology'),
(3, 'Sales'),
(4, 'Finance');

---------------------------------------------------------
-- TABLE: employees
---------------------------------------------------------
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER,
    salary INTEGER,
    hire_date TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

INSERT INTO employees (id, first_name, last_name, department_id, salary, hire_date) VALUES
(1, 'Alice', 'Moore', 3, 62000, '2020-03-10'),
(2, 'Brandon', 'Lee', 2, 78000, '2019-08-15'),
(3, 'Chen', 'Wang', 1, 54000, '2021-01-20'),
(4, 'Diana', 'Lopez', 3, 59000, '2018-11-05'),
(5, 'Evan', 'Carter', 2, 88000, '2017-06-01'),
(6, 'Fatima', 'Hassan', 4, 71000, '2022-02-17'),
(7, 'George', 'Smith', 4, 94000, '2016-09-30'),
(8, 'Hannah', 'Kim', 1, 51000, '2023-05-07'),
(9, 'Ian', 'Patel', 2, 83000, '2019-12-12'),
(10, 'Julia', 'Martinez', 3, 60000, '2020-07-19');

---------------------------------------------------------
-- TABLE: projects
---------------------------------------------------------
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    budget INTEGER
);

INSERT INTO projects (id, project_name, budget) VALUES
(1, 'CRM Upgrade', 150000),
(2, 'Website Redesign', 95000),
(3, 'Payroll Automation', 120000),
(4, 'Cloud Migration', 300000);

---------------------------------------------------------
-- TABLE: employee_projects (many-to-many)
---------------------------------------------------------
CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

INSERT INTO employee_projects (employee_id, project_id) VALUES
(1, 1),
(2, 4),
(3, 3),
(4, 1),
(5, 4),
(6, 2),
(7, 4),
(8, 3),
(9, 2),
(10, 1);
