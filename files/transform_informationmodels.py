import json
import re
import argparse
from datetime import datetime
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform(inputfile, inputfile_enh, inputfile_mongo):
    # Transforming according to rules in README
    info_models = openfile(inputfile)
    info_models_enh = openfile(inputfile_enh)
    mongo_ids = openfile(inputfile_mongo)
    models_map = openfile("models_map.json")
    identifier_map = openfile(f"identifier_map_{ os.environ['NAMESPACE']}.json")

    array = info_models["hits"]["hits"]
    array_enh = info_models_enh["hits"]["hits"]

    print("Number of info_models:" + str(len(array)))
    print("Number of info_models_enh:" + str(len(array_enh)))
    transformed = {}
    failed = {}
    for information_model in array:
        uri = information_model["_source"].get("harvestSourceUri")
        identifier = information_model["_source"].get("uniqueUri")
        if "https://fdk-dev-altinn.appspot.com/api/v1/schemas" in uri:
            service_code_list = re.findall('schemas(\\d+)', uri)
            if len(service_code_list) == 0 or len(service_code_list) > 1:
                failed[uri] = "Failed to find service code in URI"
            else:
                service_code = service_code_list[0]
                mongo_data = mongo_ids.get(service_code)
                if mongo_data:
                    if len(mongo_data) > 1:
                        if service_code in models_map:
                            key = f'https://altinn-model-publisher.digdir.no/models/{models_map[service_code]["new-id"]}'
                            transformed[key] = fields_to_change(information_model)
                        else:
                            failed[service_code] = "Not found in models_map"
                    elif len(mongo_data) == 0:
                        failed[service_code] = "Empty"
                    else:
                        transformed[mongo_data[0]] = fields_to_change(information_model)
                else:
                    failed[service_code] = "None"
        elif mongo_ids.get(identifier):
            transformed[identifier] = fields_to_change(information_model)
        elif identifier_map.get(identifier):
            transformed[identifier_map[identifier]] = fields_to_change(information_model)
        else:
            failed[identifier] = "Not found in mongo"

    for information_model in array_enh:
        uri = information_model["_source"].get("harvestSourceUri")
        harvest = information_model["_source"].get("harvest")
        identifier = information_model["_source"].get("uniqueUri")
        if "https://fdk-dev-altinn.appspot.com/api/v1/schemas" in uri:
            service_code_list = re.findall('schemas(\\d+)', uri)
            if len(service_code_list) == 0 or len(service_code_list) > 1:
                failed[uri] = "Failed to find service code in URI"
            else:
                service_code = service_code_list[0]
                mongo_data = mongo_ids.get(service_code)
                if mongo_data:
                    if len(mongo_data) > 1:
                        if service_code in models_map:
                            key = f'https://altinn-model-publisher.digdir.no/models/{models_map[service_code]["new-id"]}'
                            transformed[key] = fields_to_change(information_model)
                        else:
                            failed[service_code] = "Not found in models_map"
                    elif len(mongo_data) == 0:
                        failed[service_code] = "Empty"
                    else:
                        transformed[mongo_data[0]] = fields_to_change(information_model)
                else:
                    failed[service_code] = "None"
        elif mongo_ids.get(identifier):
            transformed[identifier] = fields_to_change(information_model)
        elif identifier_map.get(identifier):
            transformed[identifier_map[identifier]] = fields_to_change(information_model)
        else:
            failed[identifier] = "Not found in mongo"

    failed_transform = args.outputdirectory + "failed_transform.json"
    with open(failed_transform, 'w', encoding="utf-8") as failed_file:
        json.dump(failed, failed_file, ensure_ascii=False, indent=4)
    return transformed


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def fields_to_change(elastic_information_model):
    return {"fdkId": elastic_information_model["_id"],
            "issued": date_string_to_long(elastic_information_model["_source"]["harvest"]["firstHarvested"]),
            "modified": date_string_to_long(elastic_information_model["_source"]["harvest"]["lastChanged"])}


def date_string_to_long(date_string):
    return f'{int(datetime.fromisoformat(date_string).timestamp())}000'


inputfileName = args.outputdirectory + "informationmodels.json"
inputfileNameEnh = args.outputdirectory + "informationmodels_enh.json"
inputfileNameMongo = args.outputdirectory + "mongo_infmodels_id.json"
outputfileName = args.outputdirectory + "informationmodels_transformed.json"


# Transform the organization object to publisher format:
with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, inputfileNameEnh, inputfileNameMongo), outfile, ensure_ascii=False, indent=4)
