""" Dump data from a MongoDB database with static and known fields """


import sys
import json
import csv
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    has_mongo_client = True
except ImportError:
    has_mongo_client = False

def flattenjson( b, delim ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def mongo_read_write():

    try:
        mc = MongoClient('Cybertron', 27017)
        print("Connected Successfully")
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDb.")
        sys.exit(1)

    dbh = mc["pytest"]

    docs = dbh.tweetest.find({}, {"_id": 0})
    docs_count = docs.count()
    
    if docs_count > 0:
        print("%d results found." % docs_count)
    else:
        print("No results.")

    df_final = pd.DataFrame(json_normalize(list(docs)))
    # print(df_final.head())
    
    df_final.to_csv(fname, sep = ",", encoding = "utf-8")

fname = "lasthope.csv"
mongo_read_write()