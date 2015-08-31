import sys
import os
import pprint

file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
lib_path = os.path.join(dir_path, "lib")

sys.path.insert(0, lib_path)

import pymongo

#import urllib2, renamed to urllib.request in python3.X
import urllib.parse
import urllib.request

#import cookielib, renamed to http.cookiejar in python3.X
import http.cookiejar

import random
import re
import string
import getopt

# this is a validation program to make sure that the blog works correctly.
# If you are reading this in clear text, you are probably violating the honor code


# declare the variables to connect to db
connection = None
db = None

webhost = "localhost:8082"
mongostr = "mongodb://localhost:27017"
db_name = "blog"

# command line arg parsing to make folks happy who want to run at mongolabs or mongohq
# this functions uses global vars to communicate. forgive me.
def arg_parsing(argv):

    global webhost
    global mongostr
    global db_name

    try:
        opts, args = getopt.getopt(argv, "-p:-m:-d:")
    except getopt.GetoptError:
        print("usage validate.py -p webhost -m mongoConnectString -d databaseName")
        print("\twebhost defaults to {0}".format(webhost))
        print("\tmongoConnectionString default to {0}".format(mongostr))
        print("\tdatabaseName defaults to {0}".format(db_name))
        sys.exit(2)
    for opt, arg in opts:
        if (opt == '-h'):
            print("usage validate.py -p webhost -m mongoConnectString -d databaseName")
            sys.exit(2)
        elif opt in ("-p"):
            webhost = arg
            print("Overriding HTTP host to be ", webhost)
        elif opt in ("-m"):
            mongostr = arg
            print("Overriding MongoDB connection string to be ", mongostr)
        elif opt in ("-d"):
            db_name = arg
            print("Overriding MongoDB database to be ", db_name)


# check to see if they loaded the data set
def check_for_data_integrity():

    posts = db.posts
    try:
        count = posts.count()
    except:
        print("can't query MongoDB..is it running?")
        raise
        return False

    if (count != 1000):
        print("There are supposed to be 1000 documents. you have ", count)
        return False

    # find the most popular tags
    try:

        result = db.posts.aggregate([{'$project':{'tags':1}},
                                     {'$unwind':'$tags'},
                                     {'$group':{'_id': '$tags',
                                                'count':{'$sum':1}}},
                                     {'$sort':{'count':-1}},
                                     {'$limit':10}])
    except:
        print("can't query MongoDB..is it running?")
        raise
        return False

    found = False
    for item in result:
        if (item['count'] == 13 and
            item['_id'] == "sphynx"):
            found = True

    if not found:
        print("The dataset is not properly loaded. The distribution of post tags is wrong.")
        return False

    print("Data looks like it is properly loaded into the posts collection")

    return True


def check_for_fast_blog_home_page():

    posts = db.posts

    try:
        explain = posts.find().sort('date', direction=-1).limit(10).explain()
    except:
        print("can't query MongoDB..is it running?")
        raise
        return False

    if (explain['executionStats']['totalDocsExamined'] > 10):
        print("Sorry, executing the query to display the home page is too slow. ")
        print("We should be scanning no more than 10 documents. You scanned", explain['executionStats']['totalDocsExamined'])
        print("here is the output from explain")

        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(explain)
        return False

    print("Home page is super fast. Nice job.")
    return True

def get_the_middle_permalink():
    posts = db.posts
    try:
        c = posts.find().skip(500).limit(1)
        for doc in c:
            permalink = doc['permalink']
            return permalink
    except:
        print("can't query MongoDB..is it running?")
        raise
    return ""




def check_for_fast_blog_entry_page():

    posts = db.posts

    permalink = get_the_middle_permalink()
    try:
        explain = posts.find({'permalink':permalink}).explain()
    except:
        print("can't query MongoDB..is it running?")
        raise
        return False

    if (explain['executionStats']['totalDocsExamined'] > 1):
        print("Sorry, executing the query to retrieve a post by permalink is too slow ")
        print("We should be scanning no more than 1 documents. You scanned", explain['executionStats']['totalDocsExamined'])
        print("here is the output from explain")

        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(explain)
        return False

    print("Blog retrieval by permalink is super fast. Nice job.")
    return True


def check_for_fast_posts_by_tag_page():
    posts = db.posts

    tag = "sphynx"
    try:
        explain = posts.find({'tags':tag}).sort('date', direction=-1).limit(10).explain()
    except:
        print("can't query MongoDB..is it running?")
        raise
        return False

    if (explain['executionStats']['totalDocsExamined'] > 10):
        print("Sorry, executing the query to retrieve posts by tag is too slow.")
        print("We should be scanning no more than 10 documents. You scanned", explain['executionStats']['totalDocsExamined'])
        print("here is the output from explain")

        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(explain)
        return False

    print("Blog retrieval by tag is super fast. Nice job.")
    return True




def validate_hw_4_3():

    global connection
    global db

    print("Welcome to the HW 4.3 Checker. My job is to make sure you added the indexes")
    print("that make the blog fast in the following three situations")
    print("\tWhen showing the home page")
    print("\tWhen fetching a particular post")
    print("\tWhen showing all posts for a particular tag")

    # connect to the db (mongostr was set in arg_parsing)
    try:
        connection = pymongo.MongoClient(mongostr)
        db = connection[db_name]
    except Exception as e:
        print("can't connect to MongoDB using", mongostr, ". Is it running?")
        print("Exception was", e)
        sys.exit(1)

    if (not check_for_data_integrity()):
        print("Sorry, the data set is not loaded correctly in the posts collection")
        sys.exit(1)

    if (not check_for_fast_blog_home_page()):
        print("Sorry, the query to display the blog home page is too slow.")
        sys.exit(1)

    if (not check_for_fast_blog_entry_page()):
        print("Sorry, the query to retrieve a blog post by permalink is too slow.")
        sys.exit(1)

    if (not check_for_fast_posts_by_tag_page()):
        print("Sorry, the query to retrieve all posts with a certain tag is too slow")
        sys.exit(1)

    # if you are reading this in cleartext, you are violating the honor code.
    # You can still redeem yourself. Get it working and don't submit the validation code until you do.
    # All a man has at the end of the day is his word.
    print("Tests Passed for HW 4.3. Your HW 4.3 validation code is 893jfns29f728fn29f20f2")


if __name__ == "__main__":

    argv = sys.argv[1:]

    arg_parsing(argv)
    # global connection
    # global db


    validate_hw_4_3()




