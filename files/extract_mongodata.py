import json
import requests
import os
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/datasetCatalog?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester
ids = db.informationmodel.find({}, {"_id": 1}).get("_id")


with open(args.outputdirectory + 'mongo_infmodels_id.json', 'w', encoding="utf-8") as outfile:
    json.dump(ids.json(), outfile, ensure_ascii=False, indent=4)
