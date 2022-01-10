import json
import argparse
from hashlib import sha1
import os

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

inputfileName = args.outputdirectory + "infmodelsMeta.json"
outputfileName = args.outputdirectory + "transformed_models.json"
dataservices_filename = args.outputdirectory + "dataservices.json"
old_models_filename = args.outputdirectory + "old_models.json"


def transform(inputfile):
    info_models = openfile(inputfile)
    dataservices = openfile(dataservices_filename)
    transformed_models = {}
    old_models = []
    for endpoint_description in dataservices:
        old_id = create_dataservice_id(endpoint_description)
        new_id = create_dataservice_id(f'{dataservices[endpoint_description]} {endpoint_description}')
        old_meta = info_models[old_id]
        new_meta = info_models[new_id]
        old_models.append(old_id)
        transformed_models[new_id] = transform_model(old_meta, new_meta)
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


def create_dataservice_id(sha1_input: str) -> str:
    """Generate ID for model."""
    return (
            os.getenv(
                "FDK_PUBLISHERS_BASE_URI"
            )
            + "/fdk-model-publisher/catalog/"
            + sha1(bytes(sha1_input, encoding="utf-8")).hexdigest()  # noqa
    )


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)
