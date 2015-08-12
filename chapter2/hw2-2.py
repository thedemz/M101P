import sys
import os

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
lib_path = os.path.join(dir_path, "lib")

sys.path.insert(0, lib_path)

import pymongo


# connnecto to the db on standard port
connection = pymongo.MongoClient("mongodb://localhost")

db = connection.students                 # attach to db

def get_students():

    collection = db.grades         # specify the colllection

    print("There are 200 students")
    print("There should be 800 grades")
    grades = collection.find().count()

    print("Counted Grades:", grades)

    result = collection.find({'type': 'homework'}, {"student_id": 1, "score": 1, "type":1, "_id": 1}).sort(
        [("student_id", 1), ("score", 1)]
        )

    print("Counted With type Homework:", result.count())


    return result


def mark_lowest_score( grades ):

    collection = db.grades         # specify the colllection

    student_id = None

    for ix in grades:
        ix["lowest"] = False

        print(student_id, ix["student_id"])
        if student_id != ix["student_id"]:
            student_id = ix["student_id"]

            ix["lowest"] = True

            print("True")
        else:
            print("False")

        collection.save( ix )

def delete_lowest():

    collection = db.grades         # specify the colllection
    grades = collection.find().count()

    if grades == 800:
        print("Removing lowest grades from total", grades)

        collection.remove({"lowest": True})

    else:

        print("Already deleted!", grades)

if __name__ == "__main__":

    print("import the data with:")

    grades = get_students()

    mark_lowest_score(grades)

    delete_lowest()
