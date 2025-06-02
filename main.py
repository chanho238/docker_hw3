from fastapi import FastAPI
from pydantic import BaseModel, validator, Field
from typing import List

app = FastAPI()

GRADE_MAP = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int = Field(..., gt=0)  # 0 이하 거부
    grade: str

    @validator("grade")
    def validate_grade(cls, g):
        if g.upper() not in GRADE_MAP:
            raise ValueError(f"Invalid grade: {g}")
        return g.upper()

class Student(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.post("/summary")
def calculate_summary(student: Student):
    total_credits = 0
    total_points = 0.0

    for course in student.courses:
        grade_point = GRADE_MAP.get(course.grade.upper(), 0.0)
        total_credits += course.credits
        total_points += grade_point * course.credits

    gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    return {
        "student_summary": {
            "student_id": student.student_id,
            "name": student.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }

