"""Employee endpoints. Reading is public; writing needs a valid X-API-Key header."""
from fastapi import APIRouter, Depends

from app.schemas import Employee, EmployeeCreate
from app.security import verify_api_key
from app.service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])
service = EmployeeService()

# Adding this list to a route makes FastAPI run verify_api_key first.
# If the key is missing or wrong, the route body never runs.
PROTECTED = [Depends(verify_api_key)]

# Error responses listed here also show up in Swagger UI next to each endpoint.
AUTH_ERRORS = {401: {"description": "X-API-Key header is missing"},
               403: {"description": "X-API-Key header is wrong"}}
NOT_FOUND = {404: {"description": "No employee with this id"}}


@router.get("", response_model=list[Employee])
def get_employees():
    """Public - no key needed."""
    return service.list_all()


@router.post("", response_model=Employee, status_code=201, dependencies=PROTECTED,
             responses=AUTH_ERRORS)
def create_employee(employee: EmployeeCreate):
    """Protected - needs X-API-Key."""
    return service.create(employee)


@router.put("/{employee_id}", response_model=Employee, dependencies=PROTECTED,
            responses={**AUTH_ERRORS, **NOT_FOUND})
def update_employee(employee_id: int, employee: EmployeeCreate):
    """Protected - needs X-API-Key."""
    return service.update(employee_id, employee)


@router.delete("/{employee_id}", status_code=204, dependencies=PROTECTED,
               responses={**AUTH_ERRORS, **NOT_FOUND})
def delete_employee(employee_id: int):
    """Protected - needs X-API-Key."""
    service.delete(employee_id)
