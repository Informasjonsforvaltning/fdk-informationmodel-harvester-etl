import json
import os
from pymongo import MongoClient
import argparse
import bson


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/datasetCatalog?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester

with open(args.outputdirectory + 'mongo_infmodels.json') as extracted_file:
    extracted_json = json.load(extracted_file)
    for mongo_id in extracted_json:
        print("Mongo_id: " + mongo_id)
        values = extracted_json[mongo_id]
        to_be_updated = {"fdkId": str(values["fdkId"]),
                         "issued": bson.Int64(int(values["issued"])),
                         "modified": bson.Int64(int(values["modified"]))}
        print("To be updated: " + str(to_be_updated))
        print(db.informationModelMeta.find_one_and_update({'_id': mongo_id},  {'$set': to_be_updated}))

with open(args.outputdirectory + 'mongo_catalogs.json') as extracted_file:
    extracted_json = json.load(extracted_file)
    for mongo_id in extracted_json:
        print("Mongo_id: " + mongo_id)
        values = extracted_json[mongo_id]
        to_be_updated = {"fdkId": str(values["fdkId"]),
                         "issued": bson.Int64(int(values["issued"])),
                         "modified": bson.Int64(int(values["modified"]))}
        print("To be updated: " + str(to_be_updated))
        print(db.catalogMeta.find_one_and_update({'_id': mongo_id},  {'$set': to_be_updated}))
