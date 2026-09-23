from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List


# Create FastAPI application
app = FastAPI(
    title="Employee REST API",
    description="REST API for Employee Management",
    version="1.0.0"
)


# ============================================================
# PYDANTIC MODELS
# ============================================================

# Model used when creating/updating an employee
class EmployeeRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    department: str
    designation: str


class Employee(EmployeeRequest):
    id: int


# ============================================================
# TEMPORARY EMPLOYEE DATA
# ============================================================

employees: List[Employee] = [
    Employee(
        id=1,
        name="Rahul Sharma",
        email="rahul@example.com",
        phone="9876543210",
        department="IT",
        designation="Software Developer"
    ),
    Employee(
        id=2,
        name="Priya Singh",
        email="priya@example.com",
        phone="9876543211",
        department="HR",
        designation="HR Executive"
    )
]


# ============================================================
# 1. GET ALL EMPLOYEES
# ============================================================

@app.get("/employees")
def get_employees():
    return {
        "success": True,
        "data": employees
    }


# ============================================================
# 2. GET EMPLOYEE BY ID
# ============================================================

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    employee = next(
        (emp for emp in employees if emp.id == employee_id),
        None
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "success": True,
        "data": employee
    }


# ============================================================
# 3. CREATE NEW EMPLOYEE
# ============================================================

@app.post("/employees", status_code=201)
def create_employee(employee_data: EmployeeRequest):

    # Generate new ID
    if employees:
        new_id = max(emp.id for emp in employees) + 1
    else:
        new_id = 1

    new_employee = Employee(
        id=new_id,
        **employee_data.model_dump()
    )

    employees.append(new_employee)

    return {
        "success": True,
        "message": "Employee created successfully",
        "data": new_employee
    }


# ============================================================
# 4. UPDATE EMPLOYEE
# ============================================================

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_data: EmployeeRequest
):

    employee = next(
        (emp for emp in employees if emp.id == employee_id),
        None
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Update employee details
    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.phone = employee_data.phone
    employee.department = employee_data.department
    employee.designation = employee_data.designation

    return {
        "success": True,
        "message": "Employee updated successfully",
        "data": employee
    }


# ============================================================
# 5. DELETE EMPLOYEE
# ============================================================

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    employee = next(
        (emp for emp in employees if emp.id == employee_id),
        None
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employees.remove(employee)

    return {
        "success": True,
        "message": "Employee deleted successfully"
    }


# ============================================================
# ROOT API
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Employee REST API is running"
    }