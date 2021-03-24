import json
import re
import argparse
from pymongo import MongoClient
import gridfs
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
namespace = os.environ['NAMESPACE']
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/informationModelHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester

db.fs.files.find({"isPartOf": f"{uri}"}, {"fdkId": 1})

db.fs.chunks.find({"isPartOf": f"{uri}"}, {"fdkId": 1})


def transform(inputfile):
    filenames = openfile(inputfile)
    files = []
    for filename in filenames:
        files.append(db.fs.files.find({"filename": f"{filename}"}, {"_id": 1}))
    return files


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "filenames.json"
outputfileName = args.outputdirectory + "gridfs_ids.json"


# Transform the organization object to publisher format:
with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)
