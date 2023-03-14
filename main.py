from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
from pymongo.server_api import ServerApi
app = FastAPI()

# mongo client
client = pymongo.MongoClient(
    "mongodb+srv://yaadava_kishore:dMULvlVpDlLfT5Nc@stnt.qfx8k6g.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# current database will be stnt2
db = client["stnt2"]
# groups_data collection
groups_data = db["groups_data"]


class Student(BaseModel):
    name: str
    id: int


class Group(BaseModel):
    name: str
    id: int
    student1: Student
    student2: Student
    student3: Student


class RegisteredProject(BaseModel):
    name: str
    group_id: int


# home route
@app.get("/")
def read_root():
    return {"project": "FastAPI server", "group-name": "Rx100", "group-id": 1}


# group registration
@app.post("/register_group/")
async def register_group(group: Group):
    try:
        groups_data.insert_one({
            "name": group.name,
            "id": group.id,
            "student1": {
                "name": group.student1.name,
                "id": group.student1.id
            },
            "student2": {
                "name": group.student2.name,
                "id": group.student2.id
            },
            "student3": {
                "name": group.student3.name,
                "id": group.student3.id
            },
        })
        return "Group registration successful!"
    except:
        return "Error has occured!"


# all groups data fetching
@app.get("/group_details")
def group_details():
    all_groups = list(groups_data.find({}, {'_id': 0}))
    return all_groups


# group data fetching with id
@app.get("/group_details/{group_id}")
def group_details(group_id: int):
    try:
        data = groups_data.find_one({"id": group_id}, {'_id': 0})
        if (data != None):
            return data
        else:
            raise Exception()
    except:
        return f"Group with id: {group_id} wasn't registered!"

# group members data fetching
@app.get("/group_members/{group_id}")
def group_members(group_id: int):
    data = groups_data.find_one({"id": group_id}, {'_id': 0})
    student_data = {
        "student1": {"name": data["student1"]["name"], "id": data["student1"]["id"]},
        "student2": {"name": data["student2"]["name"], "id": data["student2"]["id"]},
        "student3": {"name": data["student3"]["name"], "id": data["student3"]["id"]}
    }
    return student_data
