#!/usr/bin/env python3

from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a table to persist the attributes off Department instances."""
        sql = """
                CREATE TABLE IF NOT EXISTS departments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL)
                """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists the Department instances"""
        sql = """DROP TABLE IF EXISTS departments"""

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def save(self):
        """Insert a new row with the name and location values of the current Department instance
            Update object id attribute using the primary key of the new row"""
        sql = """
        INSERT INTO departments (name, location)
        VALUES (?,?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid

Department.drop_table()
Department.create_table()

payroll = Department("Payroll", "Building A, 5th Floor")
print(payroll)  # <Department None: Payroll, Building A, 5th Floor>

hr = Department.create("Human Resources", "Building C, East Wing")
hr = Department.create("Human Resources", "Building C, East Wing")
hr = Department.create("Software Resources", "Building C, East Wing")

print(hr)  # <Department 2: Human Resources, Building C, East Wing>

payroll.save()  # Persist to db, assign object id attribute
print(payroll)  # <Department 1: Payroll, Building A, 5th Floor>

hr = Department("Human Resources", "Building C, East Wing")
print(hr)  # <Department None: Human Resources, Building C, East Wing>

hr.save()  # Persist to db, assign object id attribute
print(hr)  # <Department 2: Human Resources, Building C, East Wing>


hr.name = 'HR'
hr.location = "Building F, 10th Floor"
hr.update()
print(hr)  # <Department 2: HR, Building F, 10th Floor>

print("Delete Payroll")
payroll.delete()  # delete from db table, object still exists in memory
print(payroll)  # <Department 1: Payroll, Building A, 5th Floor>