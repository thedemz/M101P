import sys
import os
from operator import itemgetter

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)
lib_path = os.path.join(dir_path, "lib")

sys.path.insert(0, lib_path)

import pymongo


# connnecto to the db on standard port
connection = pymongo.MongoClient("mongodb://localhost")

db = connection["school"] # attach to db school

def get_student_scores():

    collection = db.students

    result = collection.find({"scores.type": "homework"}, {"scores": 1, "_id": 1}).sort([("scores.score",1),])

    print("Students with homework", result.count())

    return result

def remove_lowest_score( student_scores, score_type="homework" ):

    collection = db.students

    for ix in student_scores:

        homework = [sc for sc in ix["scores"] if sc["type"] == score_type]

        print(ix["_id"], homework)

        if len(homework) > 1:

            sorted_homework = sorted(homework, key=itemgetter("score"))

            print(ix["_id"], sorted_homework)

            lowest = sorted_homework[0]

            print(ix["scores"])

            ix["scores"].remove(lowest)

            print(ix["scores"])

            collection.update_one({"_id": ix["_id"]}, {"$set": {"scores": ix["scores"]}})


def verify_task():
    collection = db.students

    print("""To verify that you have completed this task correctly, provide the identity (in the form of their _id) of the student with the highest average in the class with following query that uses the aggregation framework.
    The answer will appear in the _id field of the resulting document.""")

    # As python dictionaries don’t maintain order you should use SON or collections.OrderedDict where explicit ordering is required eg “$sort”

    from bson.son import SON

    pipeline = [
        {"$unwind": "$scores"},
        {'$group' : {'_id' : '$_id', 'average' : {"$avg" : '$scores.score'}}},
        {"$sort": SON([("average", -1),])},
        {"$limit": 1}
    ]

    result = collection.aggregate( pipeline )

    #mongo client:
    #result = collection.aggregate( { '$unwind' : '$scores' } , { '$group' : { '_id' : '$_id' , 'average' : { "$avg" : '$scores.score' } } } , { '$sort' : { 'average' : -1 } } , { '$limit' : 1 } )

    for ix in result:
        print(ix)




if __name__ == "__main__":

    print("import the data with:")

    print("mongoimport -d school -c students < ./data/students.json")

    print("use school")
    print("db.students.count()", "should be 200.")

    student_scores = get_student_scores()

    remove_lowest_score( student_scores )

    verify_task()
