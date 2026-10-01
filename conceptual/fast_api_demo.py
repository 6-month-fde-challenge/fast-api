from fastapi import FastAPI

app = FastAPI()

@app.get("/intro")
def fast_api_intro():
    return "Fast api intro function"


@app.get("/course-details")
def get_course_details():
    return "We are in FasAPI course of whole 6 month FDE challenge course.."


@app.get("/course/{course_id}")
def get_course_details(course_id:str):
    print(f"input is : {course_id}")
    if course_id == "1":
        return f"The course aligned for the course id {course_id} is Python Fast API"
    elif course_id == "2":
        return f"The course aligned for the course id {course_id} is Python with GIT and Docker"
    elif course_id == "3":
        return f"The course aligned for the course id {course_id} is Advanced Python"
    else:
        return "Wrong input"

from pydantic import BaseModel , Field

class Mentor(BaseModel):
    user_name:str
    pass_word:str
    mentor_id:int = Field(gt=0)


@app.post("/login")
def login(mentor:Mentor):
    if mentor.user_name == "admin" and mentor.pass_word == "admin258":
        return "Logged in succesfully"