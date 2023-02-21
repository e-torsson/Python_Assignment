import requests
from api import Name, Course, Info


"""
TODO 
show the corresponding name and course, id 1 in Name show id 1 in Course
--make use of the Info class--
"""

def url(route: str):
    return f"http://127.0.0.1:8000{route}"

def menu():
    print(
    """
    1: Add 
    2: Get
    3: Delete 
    4: Update
    5: Exit  
    """)

#show all entries in the Name table
def get_names():
    all_names = []
    resp = requests.get(url("/names"))
    if not resp.status_code == 200:
        return
    data = resp.json()
    for name in data:
        name = Name(**name)    
        print("_____________")
        print(f"ID: {name.id}")
        print(f"Name: {name.name}")
        all_names.append(name)
    return all_names

# Get the name with the corresponding id from the Name table
def get_one_name(id: int):
        resp = requests.get(url(f"/names/{id}"))
        if not resp.status_code == 200:
            return
        data = resp.json()
        for name in data:
            name = Name(**name)
            print(f"ID: {name.id}")
            print(f"Name: {name.name}")
        return

# show all entries in the Course table
def get_course():
    all_courses = []
    resp = requests.get(url("/courses"))
    if not resp.status_code == 200:
        return
    
    data = resp.json()
    for course in data:
        course = Course(**course)
        print("_____________")
        print(f"ID: {course.id}")
        print(f"Course: {course.course_name}")
        all_courses.append(course)
    return all_courses

# Get the course with the corresponding id fron the Course table
def get_one_course(id: int):
    resp = requests.get(url(f"/courses/{id}"))
    if not resp.status_code == 200:
        return
    data = resp.json()
    for course in data:
        course = Course(**course)
        print(f"ID: {course.id}")
        print(f"Course: {course.course_name}")
    return

# fill with data.json data
def fill_db():
    resp = requests.post(url("/fill"))
    print(resp)

# create a new name in Name table  
def add_name():
    name = input("Enter name: ")
    entry = Name(name=name)
    
    resp = requests.post(url("/create_name"), json=entry.dict())
    print(resp)

# create a course in Course table
def add_course():
    course = input("Enter course name: ")
    entry = Course(course_name=course)
    
    resp = requests.post(url("/create_course"), json=entry.dict())
    print(resp)

# update in Name table
def update_name():
    update_name_id = input("ID of name to update: ")
    if not str.isdigit(update_name_id):
        print("Unable to find that ID")
        return
    
    name  = input("Enter new name: ")
    add_new_name = Name(name=name)
    resp = requests.put(url(f"/update_name/{update_name_id}"), json=add_new_name.dict())
    print(resp.json())

# update in Course table
def update_course():
    update_course_id = input("ID of course to update: ")
    if not str.isdigit(update_course_id):
        print("Unable to find that ID")
        return
    
    course = input("Enter new course: ")      
    add_new_course = Course(course_name=course)
    resp = requests.put(url(f"/update_course/{update_course_id}"), json=add_new_course.dict())
    print(resp.json())
            
# delete from Name table
def delete_name():
    delete_name_id = input("ID of name to delete: ")
    if not str.isdigit(delete_name_id):
        print("Invalid ID")
        return
    requests.delete(url(f"/delete_name/{delete_name_id}"))

# delete from Course table
def delete_course():
    delete_course_id = input("ID of course to delete: ")
    if not str.isdigit(delete_course_id):
        print("Invalid ID")
        return
    requests.delete(url(f"/delete_course/{delete_course_id}"))



#main
def main():
    menu()
    user_input = input("Select: ")
    if not str.isdigit(user_input):
        print("Enter valid option")
    
    # Flow controll to the menu function to give the user different options    
    match int(user_input):
        case 1:
            choice = input("Fill database (1), add to Name (2), add to Course (3): ")
            if choice == "1":
                fill_db()
            elif choice == "2":
                add_name()
            elif choice == "3":
                add_course()
            else:
                print("Invalid number")
                
                
        case 2:
            choice = input("Show Name table (1) or show Course table (2): ")      
            if choice == "1":
                choice = input("Show the whole table (1) show specific name ID (2): ")
                if choice == "1":
                    get_names()
                elif choice == "2":
                    input_id = int(input("Input ID of the name you are looking for: "))
                    get_one_name(input_id)      
            elif choice == "2":
                choice = input("Show the whole table (1) show specific course ID (2): ")
                if choice == "1":
                    get_course()
                elif choice == "2":
                    input_id = int(input("Input ID of the course you are looking for: "))
                    get_one_course(input_id)     
            else:
                print("Invalid number")
                
                
        case 3:
            choice = input("Delete from Name (1), delete from Course (2): ")
            if choice == "1":
                delete_name()
            elif choice == "2":
                delete_course()
            else:
                print("Invalid number")
                
                
        case 4:
            choice = input("Update Name (1), update Course (2): ")
            if choice == "1":
                update_name()
            elif choice == "2":
                update_course()
            else:
                print("Invalid input")
                
                
        case 5:
            exit()

while __name__ == "__main__":
    main()