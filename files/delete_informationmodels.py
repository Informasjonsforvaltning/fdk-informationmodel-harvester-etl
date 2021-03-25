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
staging_catalogs = [{"_id": "https://www.altinn.no/models/altinn", "fdkId": "f27930d7-8070-3d12-b4c7-e6aae22a478f"},
                    {"_id": "https://www.altinn.no/models/or", "fdkId": "73925a02-21a0-3ad9-948c-ac017299ec22"},
                    {"_id": "https://www.altinn.no/models/seres", "fdkId": "c62b1bd8-17a1-3724-9d00-db020a2025b8"}]
other_catalogs = [{"_id": "https://www.altinn.no/models/catalog", "fdkId": "30251da7-e78f-33e5-9249-375451c9b187"}]
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/informationModelHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester

if namespace == "staging":
    catalogs = staging_catalogs
else:
    catalogs = other_catalogs


def transform(inputfile, infmodels):
    filenames = openfile(inputfile)
    inf_models = openfile(infmodels)
    files = []
    output = []
    for filename in filenames:
        files.append(db.fs.files.find_one({"filename": f"{filename}"}, {"_id": 1}))

    for gridfsid in files:
        print(gridfsid)
        output.append(db.fs.chunks.delete_one({"_id": gridfsid}))
        output.append(db.fs.files.delete_one({"_id": gridfsid}))

    for model in inf_models:
        model_id = model["_id"]
        output.append(db.informationModelMeta.delete_one({"_id": model_id}))

    for catalog in catalogs:
        catalog_id = catalog["_id"]
        output.append(db.catalogMeta.delete_one({"_id": catalog_id}))

    return output


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "filenames.json"
infModelsMeta = args.outputdirectory + "infmodelsMeta.json"
outputfileName = args.outputdirectory + "deleted.json"


# Transform the organization object to publisher format:
with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, infModelsMeta), outfile, ensure_ascii=False, indent=4)
