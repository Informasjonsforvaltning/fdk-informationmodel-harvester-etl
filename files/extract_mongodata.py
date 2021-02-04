import json
import os
import re
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/datasetCatalog?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester
informationmodel_list = list(db.informationmodel.find({}, {"_id": 1, "fdkId": 1, "issued": 1, "modified": 1}))
catalog_list = list(db.catalog.find({}, {"_id": 1, "fdkId": 1, "issued": 1, "modified": 1}))

with open(args.outputdirectory + 'mongo_infmodels.json', 'w', encoding="utf-8") as outfile:
    json.dump(informationmodel_list, outfile, ensure_ascii=False, indent=4)

with open(args.outputdirectory + 'mongo_catalogs.json', 'w', encoding="utf-8") as outfile:
    json.dump(catalog_list, outfile, ensure_ascii=False, indent=4)
