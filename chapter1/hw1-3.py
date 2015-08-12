import sys
import os

file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
lib_path = os.path.join(dir_path,"lib")

sys.path.insert(0,lib_path)

import pymongo
import bottle

@bottle.get("/hw1/<n>")
def get_hw1(n):

    # connnecto to the db on standard port
    connection = pymongo.MongoClient("mongodb://localhost")

    n = int(n)

    db = connection.m101                 # attach to db
    collection = db.funnynumbers         # specify the colllection


    magic = 0

    try:
        iter = collection.find({},limit=1, skip=n).sort('value', direction=1)
        for item in iter:
            return str(int(item['value'])) + "\n"
    except Exception as e:
        print( "Error trying to read collection:", type(e), e)


bottle.debug(True)
bottle.run(host='localhost', port=8080)


