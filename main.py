from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

GRADE_MAP = {
    "A+": 4.5,
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class Student(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/summary")
def calculate(student: Student):
    total_credits = 0
    total_points = 0.0

    for course in student.courses:
        grade_point = GRADE_MAP.get(course.grade.upper(), 0.0)
        total_credits += course.credits
        total_points += grade_point * course.credits

    gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    result = {
        "student_summary": {
            "student_id": student.student_id,
            "name": student.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
    return result
