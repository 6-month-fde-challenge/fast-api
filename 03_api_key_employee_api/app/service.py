"""EmployeeService - keeps employees in memory. It knows nothing about API keys."""
from app.exceptions import EmployeeNotFoundError
from app.schemas import Employee, EmployeeCreate


class EmployeeService:

    def __init__(self):
        self.employees = {}
        self.next_id = 1

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(id=self.next_id, **data.model_dump())
        self.employees[employee.id] = employee
        self.next_id += 1
        return employee

    def list_all(self) -> list[Employee]:
        return list(self.employees.values())

    def update(self, employee_id: int, data: EmployeeCreate) -> Employee:
        self._check_exists(employee_id)
        employee = Employee(id=employee_id, **data.model_dump())
        self.employees[employee_id] = employee
        return employee

    def delete(self, employee_id: int) -> None:
        self._check_exists(employee_id)
        del self.employees[employee_id]

    def _check_exists(self, employee_id: int) -> None:
        if employee_id not in self.employees:
            raise EmployeeNotFoundError(employee_id)
