import pymongo
import blog
import operator

from pymongo import IndexModel, ASCENDING, DESCENDING



connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection["blog"]




if __name__ == "__main__":

    collection_names = database.collection_names(False)

    print(collection_names)

    collection = database["posts"]

    print("Dropping All Indexes for", collection.name)

    collection.drop_indexes()

    print("Creating Indexes for", collection.name, "...")

    # http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_indexes

    index1 = IndexModel([("tags", DESCENDING),("date", ASCENDING)], name="_tags_date_")
    index2 = IndexModel([("date", ASCENDING)], name="_date_")
    index3 = IndexModel([("permalink", ASCENDING)], name="_permalink_")

    collection.create_indexes([index1, index2, index3])

    info = collection.index_information()
    print(collection.name, "contains", len(info), "indexes")

    for key, value in sorted(info.items(), key=operator.itemgetter(0)):

        print(key)
        print(value)



    # for ix in collection.list_indexes():
    #     print(ix)






