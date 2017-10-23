""" An example of how to read from a MongoDB database """


import sys
from datetime import datetime

try:
    from pymongo import MongoClient
    #from pymongo import collection
    from pymongo.errors import ConnectionFailure
    has_mongo_client = True
except ImportError:
    has_mongo_client = False

def main():
    """ Connect to MongoDB """

    try:
        c = MongoClient('Cybertron', 27017)
        print("Connected Successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDb %s" % e)
        sys.exit(1)

    # Get a database handle to a database named "pytest"
    dbh = c["pytest"]
    print("Connected to database")

if __name__ == "__main__":
    main()
