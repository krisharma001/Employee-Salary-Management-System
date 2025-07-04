"""
Employee Salary Management System
Developed using Python, MySQL, and Pandas

Features:
- Database connection and data retrieval
- Salary calculations (bonus, tax, net salary)
- Automated salary slip generation
- CSV export functionality
"""

import mysql.connector
import pandas as pd
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmployeeSalaryManagement:
    def __init__(self, host='localhost', user='root', password='', database='employee_salary_management'):
        """
        Initialize the Employee Salary Management System
        
        Args:
            host (str): MySQL host
            user (str): MySQL username
            password (str): MySQL password
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.df_employees = None
        
    def connect_database(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logger.info("Successfully connected to MySQL database")
            return True
        except mysql.connector.Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            return False
    
    def fetch_employee_data(self):
        """Fetch employee data from MySQL and load into Pandas DataFrame"""
        if not self.connection:
            if not self.connect_database():
                return None
        
        try:
            query = """
            SELECT employee_id, name, basic_salary, bonus_percentage, tax_percentage
            FROM employees
            ORDER BY employee_id
            """
            
            self.df_employees = pd.read_sql(query, self.connection)
            logger.info(f"Successfully fetched {len(self.df_employees)} employee records")
            return self.df_employees
        except Exception as e:
            logger.error(f"Error fetching employee data: {e}")
            return None
    
    def calculate_salary_components(self):
        """Calculate bonus, tax, and net salary using Pandas"""
        if self.df_employees is None:
            logger.error("No employee data available. Please fetch data first.")
            return None
        
        try:
            # Calculate Bonus = Basic Salary × (Bonus Percentage / 100)
            self.df_employees['bonus'] = self.df_employees['basic_salary'] * (self.df_employees['bonus_percentage'] / 100)
            
            # Calculate Tax = Basic Salary × (Tax Percentage / 100)
            self.df_employees['tax'] = self.df_employees['basic_salary'] * (self.df_employees['tax_percentage'] / 100)
            
            # Calculate Net Salary = Basic Salary + Bonus - Tax
            self.df_employees['net_salary'] = self.df_employees['basic_salary'] + self.df_employees['bonus'] - self.df_employees['tax']
            
            # Round to 2 decimal places
            self.df_employees['bonus'] = self.df_employees['bonus'].round(2)
            self.df_employees['tax'] = self.df_employees['tax'].round(2)
            self.df_employees['net_salary'] = self.df_employees['net_salary'].round(2)
            
            logger.info("Salary components calculated successfully")
            return self.df_employees
        except Exception as e:
            logger.error(f"Error calculating salary components: {e}")
            return None
    
    def generate_salary_slips(self, output_dir='salary_slips'):
        """Generate individual salary slips in CSV format"""
        if self.df_employees is None:
            logger.error("No employee data available for salary slip generation")
            return False
        
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.info(f"Created directory: {output_dir}")
            
            # Generate individual salary slips
            for index, employee in self.df_employees.iterrows():
                # Create salary slip data
                salary_slip_data = {
                    'Employee ID': [employee['employee_id']],
                    'Name': [employee['name']],
                    'Basic Salary': [employee['basic_salary']],
                    'Bonus Percentage': [f"{employee['bonus_percentage']}%"],
                    'Bonus Amount': [employee['bonus']],
                    'Tax Percentage': [f"{employee['tax_percentage']}%"],
                    'Tax Amount': [employee['tax']],
                    'Net Salary': [employee['net_salary']],
                    'Generated Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                }
                
                # Create DataFrame for individual salary slip
                slip_df = pd.DataFrame(salary_slip_data)
                
                # Generate filename
                filename = f"salary_slip_{employee['employee_id']}.csv"
                filepath = os.path.join(output_dir, filename)
                
                # Save to CSV
                slip_df.to_csv(filepath, index=False)
                logger.info(f"Generated salary slip: {filename}")
            
            logger.info(f"All salary slips generated successfully in '{output_dir}' directory")
            return True
        except Exception as e:
            logger.error(f"Error generating salary slips: {e}")
            return False
    
    def display_salary_summary(self):
        """Display salary summary table"""
        if self.df_employees is None:
            logger.error("No employee data available")
            return
        
        print("\n" + "="*80)
        print("EMPLOYEE SALARY SUMMARY")
        print("="*80)
        print(self.df_employees.to_string(index=False))
        print("="*80)
        
        # Display statistics
        print("\nSALARY STATISTICS:")
        print(f"Total Employees: {len(self.df_employees)}")
        print(f"Total Basic Salary: ${self.df_employees['basic_salary'].sum():,.2f}")
        print(f"Total Bonus: ${self.df_employees['bonus'].sum():,.2f}")
        print(f"Total Tax: ${self.df_employees['tax'].sum():,.2f}")
        print(f"Total Net Salary: ${self.df_employees['net_salary'].sum():,.2f}")
        print(f"Average Net Salary: ${self.df_employees['net_salary'].mean():,.2f}")
        print("="*80)
    
    def export_complete_report(self, filename='complete_salary_report.csv'):
        """Export complete salary report to CSV"""
        if self.df_employees is None:
            logger.error("No employee data available for export")
            return False
        
        try:
            # Add timestamp to the report
            report_df = self.df_employees.copy()
            report_df['report_generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Export to CSV
            report_df.to_csv(filename, index=False)
            logger.info(f"Complete salary report exported to: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting complete report: {e}")
            return False
    
    def add_new_employee(self, name, basic_salary, bonus_percentage, tax_percentage):
        """Add new employee to database"""
        if not self.connection:
            if not self.connect_database():
                return False
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO employees (name, basic_salary, bonus_percentage, tax_percentage)
            VALUES (%s, %s, %s, %s)
            """
            values = (name, basic_salary, bonus_percentage, tax_percentage)
            cursor.execute(query, values)
            self.connection.commit()
            
            employee_id = cursor.lastrowid
            logger.info(f"New employee added successfully with ID: {employee_id}")
            cursor.close()
            return employee_id
        except Exception as e:
            logger.error(f"Error adding new employee: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

def main():
    """Main function to run the Employee Salary Management System"""
    print("="*60)
    print("EMPLOYEE SALARY MANAGEMENT SYSTEM")
    print("="*60)
    
    # Initialize the system
    # Note: Update the database credentials as per your MySQL setup
    salary_system = EmployeeSalaryManagement(
        host='localhost',
        user='root',
        password='your_password',  # Update with your MySQL password
        database='employee_salary_management'
    )
    
    try:
        # Step 1: Connect to database
        print("\n1. Connecting to MySQL database...")
        if not salary_system.connect_database():
            print("Failed to connect to database. Please check your credentials.")
            return
        
        # Step 2: Fetch employee data
        print("\n2. Fetching employee data...")
        if salary_system.fetch_employee_data() is None:
            print("Failed to fetch employee data.")
            return
        
        # Step 3: Calculate salary components
        print("\n3. Calculating salary components...")
        if salary_system.calculate_salary_components() is None:
            print("Failed to calculate salary components.")
            return
        
        # Step 4: Display salary summary
        print("\n4. Displaying salary summary...")
        salary_system.display_salary_summary()
        
        # Step 5: Generate individual salary slips
        print("\n5. Generating individual salary slips...")
        if salary_system.generate_salary_slips():
            print("Individual salary slips generated successfully!")
        
        # Step 6: Export complete report
        print("\n6. Exporting complete salary report...")
        if salary_system.export_complete_report():
            print("Complete salary report exported successfully!")
        
        # Optional: Add new employee example
        print("\n7. Adding new employee (Example)...")
        new_employee_id = salary_system.add_new_employee(
            name="Alex Johnson",
            basic_salary=62000.00,
            bonus_percentage=14.00,
            tax_percentage=19.00
        )
        if new_employee_id:
            print(f"New employee added with ID: {new_employee_id}")
        
        print("\n" + "="*60)
        print("SYSTEM EXECUTION COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"An error occurred during system execution: {e}")
    finally:
        # Close database connection
        salary_system.close_connection()

if __name__ == "__main__":
    main()