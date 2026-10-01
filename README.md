# FastAPI - Module 05 of the 6 Month FDE Challenge

This repository holds the FastAPI module of the
[6 month FDE (Forward Deployed Engineer) challenge](https://github.com/6-month-fde-challenge).
It has two parts:

- **[conceptual/](conceptual/)**: the lesson material. FastAPI basics, Pydantic,
  and a CRUD API backed by a PostgreSQL database.
- **Four tasks**: small, complete APIs. Each one is in its own folder with its own
  README, Swagger UI screenshots and video thumbnail.

Every task can be explored in **Swagger UI**, the interactive documentation FastAPI
builds from the code, at `http://127.0.0.1:8000/docs`.

---

## The four tasks

| # | Task | What it shows |
|---|---|---|
| 1 | [Course Enrollment API](01_course_enrollment_api/README.md) | Courses and enrollments; blocks a duplicate enrollment (409); 404 for an unknown student, course or enrollment |
| 2 | [Student CRUD API](02_student_crud_api/README.md) | Create, read, update and delete; Pydantic validation; unique email; the right status code for each outcome |
| 3 | [API Key Protected Employee API](03_api_key_employee_api/README.md) | `X-API-Key` header on the write endpoints: 401 when missing, 403 when wrong; the key is kept out of GitHub |
| 4 | [Mini E-Commerce Order API](04_ecommerce_order_api/README.md) | Products and orders; stock checks; the total is **calculated on the server**; status flow PLACED → PROCESSING → SHIPPED → DELIVERED |

| Task 1 | Task 2 |
|---|---|
| [![Course Enrollment](01_course_enrollment_api/course_enrollment.png)](01_course_enrollment_api/README.md) | [![Student CRUD](02_student_crud_api/student_crud.png)](02_student_crud_api/README.md) |
| **Task 3** | **Task 4** |
| [![API Key Security](03_api_key_employee_api/api_key_auth.png)](03_api_key_employee_api/README.md) | [![E-Commerce Orders](04_ecommerce_order_api/ecommerce_orders.png)](04_ecommerce_order_api/README.md) |

Each task folder also contains `task.txt`, the original task statement.

---

## How every task is built

All four tasks follow the same simple layout, so once you know one you know them all:

```
NN_task_name/
├── main.py              # creates the FastAPI app, adds the router and the error handler
├── requirements.txt
├── README.md            # how to run it, endpoints, validation, real requests and responses
├── task.txt             # the task statement
├── <thumbnail>.png
├── screenshots/         # real Swagger UI screenshots
└── app/                 # the application package
    ├── __init__.py
    ├── schemas.py       # Pydantic models + custom @field_validator rules
    ├── service.py       # a service class that holds the data and the business rules
    ├── routes.py        # the endpoints (APIRouter)
    └── exceptions.py    # custom exception classes + one handler that returns JSON
```

| Idea | How the tasks use it |
|---|---|
| **Modules and packages** | `app/` is a package; each module has one job: data shapes, rules, endpoints, errors. |
| **Classes and objects** | Each task has a service class (`EnrollmentService`, `StudentService`, ...) that keeps its data inside the object. |
| **Inheritance** | Response models extend request models, e.g. `Student(StudentCreate)` adds `id`. Exceptions extend one `AppError` base class. |
| **Pydantic validation** | Built-in rules (`Field(min_length=2)`, `EmailStr`) plus custom validators (clean names, lowercase emails, at most 2 decimals on money). Bad input gets a `422` that lists every failed field. |
| **Custom exceptions** | The services raise `NotFoundError`, `OutOfStockError`, ... Each class carries its own status code, and one handler turns any of them into `{"detail": "..."}`. |
| **Swagger UI** | Every route sets its success code (201, 200, 204), and every route that can fail lists its error codes, so `/docs` shows the whole contract. |

Data is kept **in memory** (plain Python dictionaries), so each task runs from a
fresh clone with no database to set up. The data resets when the server restarts.

---

## Quick start

Needs **Python 3.10 or newer**. Run any task the same way, for example Task 1:

```bash
git clone https://github.com/6-month-fde-challenge/fast-api.git
cd fast-api/01_course_enrollment_api

python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs**. Run one task at a time: they all use port 8000.

For Task 3, click **Authorize** in Swagger UI and enter the demo key
`super30-secret-key`, or set your own key in a `.env` file. Its README explains how.

---

## Conceptual material

[conceptual/](conceptual/) holds the code and slides from the FastAPI lessons.

| File | What it is |
|---|---|
| `fast_api_demo.py` | Part 1: first routes (`GET /intro`, `GET /course/{course_id}`) and a Pydantic model behind `POST /login` |
| `database.py` | Part 2: a students API on a PostgreSQL database (Neon) with SQLAlchemy: `GET`, `POST`, `PUT`, `PATCH` and `DELETE` |
| `sample.txt` | The SQL that creates and fills the `students` table, plus a copy of the Part 2 code |
| `FastAPI_Pydantic_AIwithVK.pptx` | The lesson slides |
| `fast_api_part_1.png`, `fast_api_part_2.png` | Video thumbnails for Part 1 and Part 2 |
| `requirements.txt` | Packages for the conceptual code, including `sqlalchemy` and `psycopg` |

`database.py` needs a real PostgreSQL database. It reads the connection string
from a `DATABASE_URL` entry in a `.env` file, which is **git-ignored**, so no
database password is in this repository. To run it, create your own database (for
example a free Neon project), run the SQL from `sample.txt`, and put your own
connection string in `.env`:

```
DATABASE_URL=postgresql://<user>:<password>@<host>/<database>?sslmode=require
```

```bash
cd conceptual
pip install -r requirements.txt
uvicorn database:app --reload          # or: uvicorn fast_api_demo:app --reload
```

---

## Repository layout

```
fast-api/
├── README.md                       # this file
├── 01_course_enrollment_api/
├── 02_student_crud_api/
├── 03_api_key_employee_api/
├── 04_ecommerce_order_api/
└── conceptual/
```

Not in the repository, on purpose (see [.gitignore](.gitignore)): `.env` files with
real keys or database passwords, virtual environments, and `__pycache__/`.
