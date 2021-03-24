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


def transform(inputfile, infmodels):
    filenames = openfile(inputfile)
    inf_models = openfile(infmodels)
    files = []
    output = {}
    for filename in filenames:
        files.append(db.fs.files.find({"filename": f"{filename}"}, {"_id": 1}))

    for gridfsid in files:
        print(str(gridfsid))
        output[str(gridfsid) + "-chunks"] = db.fs.chunks.remove(gridfsid)
        output[str(gridfsid) + "-files"] = db.fs.files.remove(gridfsid)

    for models in inf_models:
        model_id = inf_models[models]["_id"]
        output[str(model_id) + "-model"] = db.informationModelsMeta.remove(model_id)
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
