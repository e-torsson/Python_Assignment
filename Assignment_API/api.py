from fastapi import FastAPI
from db import DB 
from pydantic import BaseModel

# Structure the different tables pressent in the data.json file
class Name(BaseModel):
    id: int = None
    name: str

class Course(BaseModel):
    id: int = None
    course_name: str
    
class Info(BaseModel):
    name_id: int
    course_id: int
    role: int

# init FastAPI and create a database when running the file
app = FastAPI()
db = DB("test.db")
 

@app.get("/")
def root():
    return "HELLO"

# Get all names from Name table in the database
@app.get("/names")
def get_names(): 
    get_names_query = """
    SELECT * FROM Name
    """
    call = db.call_db(get_names_query)
    name_list = []
            
    for names in call:
        id, name = names
        name_list.append(Name(id=id, name=name))
            
    return name_list

# Get one name from the database
@app.get("/names/{id}")
def get_one_name(id: int):
        get_name_query = """
        SELECT * FROM Name WHERE id = ?
        """ 
        call = db.call_db(get_name_query, id)
        one_name_list = []
        
        for one_name in call:
            id, name = one_name
            one_name_list.append(Name(id=id, name=name))
        return one_name_list

# Get all the courses from Course table in the database
@app.get("/courses")
def get_course():
    get_course_query = """
    SELECT * FROM Course
    """
    call = db.call_db(get_course_query)
    course_list = []
    
    for courses in call:
        id, course = courses
        course_list.append(Course(id=id, course_name=course))
        
    return course_list

# Get one course from the database
@app.get("/courses/{id}")
def get_one_course(id: int):
    get_course_query = """
    SELECT * FROM Course WHERE id = ?
    """
    call = db.call_db(get_course_query, id)
    one_course_list = []
    
    for one_course in call:
        id, course_name = one_course
        one_course_list.append(Course(id=id, course_name=course_name))
    return one_course_list

# TODO
@app.get("/userinfo/{id}")
def get_userinfo():
    pass

# Fill the database with the json file
@app.post("/fill")
def add():
    db.data_entry()
    return True

# create a new entry in Name table
@app.post("/create_name")
def create_name(name: Name):
    post_name_query = """
    INSERT INTO Name (name) VALUES (?)
    """
    db.call_db(post_name_query, name.name)
    return True
    
# create a new entry in Course table    
@app.post("/create_course")
def create_course(course: Course):
    post_course_query = """
    INSERT INTO Course (course_name) VALUES (?)
    """
    db.call_db(post_course_query, course.course_name)
    return True
    
# update Name table
@app.put("/update_name/{id}")
def update_name(id, updated_name: Name): 
    current_names = get_names()
    index = None
    
    for i, name in enumerate(current_names):
        if name.id == int(id):
            index = i
            break
        
    if index is None:
        return "Invalid index"
    if not updated_name.name:
        updated_name.name = current_names[index]
    
    new_name_query = """
    UPDATE Name SET name = ? WHERE id = ?
    """
    db.call_db(new_name_query, updated_name.name, id)
    return True

# update Course table
@app.put("/update_course/{id}")
def update_course(id, updated_course: Course):
    current_courses = get_course()
    index = None
    
    for i, course in enumerate(current_courses):
        if course.id == int(id):
            index = i
            break
        
    if index is None:
        return "Invalid index"
    if not updated_course.course_name:
        updated_course.course_name = current_courses[index]    
    
    new_course_query = """
    UPDATE Course SET course_name = ? WHERE id = ?
    """
    db.call_db(new_course_query, updated_course.course_name, id)
    return True

# delete from Name table
@app.delete("/delete_name/{id}")
def delete_name(id):
    delete_name_query = """
    DELETE FROM Name where id = ?
    """
    db.call_db(delete_name_query, id)
    return True

# delete from Course table
@app.delete("/delete_course/{id}")
def delete_course(id):
    delete_course_query = """
    DELETE FROM Course where id = ?
    """
    db.call_db(delete_course_query, id)
    return True