import fastapi
from fastapi import Path,Query
from fastapi import FastAPI
from pydantic import BaseModel #pydantic is a data validation library and BaseModel is a class in it used to define a newly created data model 
from typing import Optional

app = FastAPI() #object creation for FastAPI class

students = {
    1 : {
        "name" : "rohan",
        "age" : 22,
        "year" : "fourth year" 
    },
    
    2: {   "name" : "rajesh",
        "age" : 21,
        "year" : "fourth year" 
        
    }
}

class Student(BaseModel):  #a new class model created to help with the structure for the POST method
    name : str
    age : int
    year : str
    
class UpdateStudent(BaseModel): #created to provide flexibility for the PUT method so that user can select and update the fields required
    name : Optional[str] = None
    age : Optional[int]  = None
    year : Optional[str] = None

@app.get("/")
def index():
    return {"name":"First Data"}

@app.get("/get-student/{student_id}") #path parameter demonstration
def get_student_details(student_id : int = Path(..., description = "Enter the id of the student")):
    return students[student_id]

#Query parameter demonstration is similar to path but instead of keyword in the link here it will be "?/something = something"
#u can achieve this by importing the Query class

@app.get("/get_student")
def get_student_details(name: str = Query(..., description="Name of the student")):
    for student_id in students:
        if students[student_id]["name"].lower() == name.lower():
            return students[student_id]
    return {"message": "Student not found"}


@app.post("/create_student/{student_id}")
def add_student(student_id : int, student : Student):
    if student_id in students:
        return "Student already exist"
    students[student_id] = student
    return students[student_id]


@app.put("/update_student/{student_id}")
def update_student(student_id : int, student : UpdateStudent):
    if student_id not in students:
        return "Invalid Id"
    
    if student.name != None:
        students[student_id].name = student.name
        
    if student.age != None:
        students[student_id].age = student.age
        
    if student.year != None:
        students[student_id].year = student.year
        
    return students[student_id]


@app.delete("/delete_id/{student_id}")
def delete_student(student_id :int):
    if student_id not in students:
        return "Invalid Id"
    del students[student_id]


