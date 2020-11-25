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
ids = "{}, {_id:1}).map(function(item){ return item._id; }"
collection = db.informationmodel.find(ids)


url = 'http://fdk-harvester-bff:8080/models'

print("Getting from the following url: ", url)
# Load the publisher by posting the data:
r = requests.get(url)
with open(args.outputdirectory + 'mongo_infmodels_id.json', 'w', encoding="utf-8") as outfile:
    json.dump(r.json(), outfile, ensure_ascii=False, indent=4)
