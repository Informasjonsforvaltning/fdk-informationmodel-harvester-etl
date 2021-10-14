import json
import argparse
from hashlib import sha1

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

inputfileName = args.outputdirectory + "infmodelsMeta.json"
outputfileName = args.outputdirectory + "transformed_models.json"
old_models_filename = args.outputdirectory + "old_models.json"


def transform(inputfile):
    info_models = openfile(inputfile)
    transformed_models = {}
    old_models = {}
    for model_id in info_models:
        new_id = create_hash(model_id)
        print("New id: " + new_id)
        for other_id in info_models:
            if new_id in other_id:
                transformed_models[other_id] = transform_model(info_models[model_id], info_models[other_id])
                old_models[model_id] = info_models[model_id]
    with open(old_models_filename, 'w', encoding="utf-8") as old_models_file:
        json.dump(old_models, old_models_file, ensure_ascii=False, indent=4)
    return transformed_models


def transform_model(old_model, new_model):
    new_model["fdkId"] = old_model["fdkId"]
    new_model["issued"] = old_model["issued"]
    return new_model


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def create_hash(old_id):
    print("Old id: " + old_id)
    return sha1(bytes(old_id, encoding="utf-8")).hexdigest()


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)
