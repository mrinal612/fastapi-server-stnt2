from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    id: int


class Group(BaseModel):
    name: str
    id: int
    student1: Student
    student2: Student
    student3: Student


groups_data = dict()


# home route
@app.get("/")
def read_root():
    return {"project": "FastAPI server", "group": 14}


# group registration
@app.post("/register_group/")
async def register_group(group: Group):
    try:
        group_id = group.id
        groups_data[group_id] = group
        return "Group registration successful!"
    except:
        return "Error has occured!"


# group data fetching with id
@app.get("/group_details/{group_id}")
def group_details(group_id: int):
    try:
        return groups_data[group_id]
    except:
        return f"group with id: {group_id} wasn't registered!"


# all groups data fetching
@app.get("/group_details")
def group_details():
    return groups_data
