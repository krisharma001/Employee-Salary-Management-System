-- Employee Salary Management System Database Script
-- Create Database
CREATE DATABASE IF NOT EXISTS employee_salary_management;
USE employee_salary_management;

-- Create Employee Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    basic_salary DECIMAL(10,2) NOT NULL,
    bonus_percentage DECIMAL(5,2) DEFAULT 0.00,
    tax_percentage DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert Sample Data
INSERT INTO employees (name, basic_salary, bonus_percentage, tax_percentage) VALUES
('John Smith', 50000.00, 10.00, 15.00),
('Sarah Johnson', 60000.00, 12.00, 18.00),
('Mike Davis', 45000.00, 8.00, 12.00),
('Emily Wilson', 55000.00, 15.00, 16.00),
('David Brown', 70000.00, 20.00, 22.00),
('Lisa Anderson', 48000.00, 9.00, 14.00),
('Robert Taylor', 65000.00, 18.00, 20.00),
('Jennifer Lee', 52000.00, 11.00, 15.00),
('Christopher White', 58000.00, 13.00, 17.00),
('Amanda Martinez', 47000.00, 7.00, 13.00);

-- Create index for better performance
CREATE INDEX idx_employee_name ON employees(name);
CREATE INDEX idx_basic_salary ON employees(basic_salary);

-- Display all records
SELECT * FROM employees;

-- Optional: Create a view for salary calculations
CREATE VIEW salary_summary AS
SELECT 
    employee_id,
    name,
    basic_salary,
    bonus_percentage,
    tax_percentage,
    ROUND(basic_salary * (bonus_percentage / 100), 2) as calculated_bonus,
    ROUND(basic_salary * (tax_percentage / 100), 2) as calculated_tax,
    ROUND(basic_salary + (basic_salary * (bonus_percentage / 100)) - (basic_salary * (tax_percentage / 100)), 2) as net_salary
FROM employees;