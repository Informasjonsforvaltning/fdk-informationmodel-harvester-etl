import json
import argparse
from pymongo import MongoClient

import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/informationModelHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester

input_fileName = args.outputdirectory + "transformed_models.json"
delete_fileName = args.outputdirectory + "old_models.json"


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


transformed_json = openfile(input_fileName)
delete_json = openfile(delete_fileName)


total_updated = 0
total_failed = 0
fail_log = {}
for mongo_id in transformed_json:
    to_be_updated = transformed_json[mongo_id]
    print("Updating ID: " + mongo_id)
    update_result = db.informationModelMeta.find_one_and_update({'_id': mongo_id}, {'$set': to_be_updated})
    if update_result:
        total_updated += 1
        print("Successfully updated: " + mongo_id)
    else:
        total_failed += 1
        print("Update failed: " + mongo_id)
        fail_log[mongo_id] = mongo_id
print("Total number of records updated: " + str(total_updated))
print("Total number of record updates failed: " + str(total_failed))
with open(args.outputdirectory + "load_errors.json", 'w', encoding="utf-8") as err_file:
    json.dump(fail_log, err_file, ensure_ascii=False, indent=4)


total_deleted = 0
total_failed = 0
fail_log = {}
for mongo_id in delete_json:
    print("Deleting ID: " + mongo_id)
    delete_result = db.informationModelMeta.delete_one({"_id": mongo_id})
    if delete_result["acknowledged"]:
        total_deleted += 1
        print("Successfully deleted: " + mongo_id)
    else:
        total_failed += 1
        print("Delete failed: " + mongo_id)
        fail_log[mongo_id] = mongo_id
print("Total number of records updated: " + str(total_updated))
print("Total number of record updates failed: " + str(total_failed))
with open(args.outputdirectory + "delete_errors.json", 'w', encoding="utf-8") as err_file:
    json.dump(fail_log, err_file, ensure_ascii=False, indent=4)
