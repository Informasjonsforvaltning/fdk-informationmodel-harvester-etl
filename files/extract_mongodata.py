import json
import os
import re
from pymongo import MongoClient
import argparse
from bson.json_util import dumps

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/datasetCatalog?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester
dict_list = list(db.informationmodel.find({}, {"_id": 1}))
ids = {}
for id_dict in dict_list:
    id_str = id_dict["_id"]
    if "https://fdk-dev-altinn.appspot.com/api/v1/schemas" in id_str:
        id_str_mod = id_str.rpartition('/')[2]
        id_str_mod_getting_there = id_str_mod.partition('-')[0]

        uriArray = ids.get(id_str_mod_getting_there)
        uriArray = uriArray if uriArray else []
        uriArray.append(id_str)
        ids[id_str_mod_getting_there] = uriArray
    else:
        ids[id_str] = id_str

with open(args.outputdirectory + 'mongo_infmodels_id.json', 'w', encoding="utf-8") as outfile:
    json.dump(ids, outfile, ensure_ascii=False, indent=4)
