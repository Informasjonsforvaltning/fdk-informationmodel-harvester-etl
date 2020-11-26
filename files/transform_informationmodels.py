import json
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform(inputfile, inputfile_enh, inputfile_mongo):
    # Transforming according to rules in README
    info_models = openfile(inputfile)
    info_models_enh = openfile(inputfile_enh)
    mongo_ids = openfile(inputfile_mongo)
    models_map = openfile("models_map.json")

    array = info_models["hits"]["hits"]
    array_enh = info_models_enh["hits"]["hits"]

    print("Number of info_models:" + str(len(array)) + "\n")
    print("Number of info_models_enh:" + str(len(array_enh)) + "\n")
    transformed = {}
    failed = {}
    for information_model in array:
        uri = information_model["_source"].get("harvestSourceUri")
        identifier = information_model["_source"].get("identifier")
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
                            transformed[service_code] = "Is OK (models_map)"
                        else:
                            failed[service_code] = "Not found in models_map"
                    elif len(mongo_data) == 0:
                        failed[service_code] = "Empty"
                    else:
                        transformed[service_code] = "Is OK"
                else:
                    failed[service_code] = "None"
        elif mongo_ids.get(identifier):
            transformed[identifier] = "Is OK (identifier)"
        else:
            failed[identifier] = "Not found in mongo"

    for information_model in array_enh:
        uri = information_model["_source"].get("harvestSourceUri")
        identifier = information_model["_source"].get("identifier")
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
                            transformed[service_code] = "Is OK (models_map)"
                        else:
                            failed[service_code] = "Not found in models_map"
                    elif len(mongo_data) == 0:
                        failed[service_code] = "Empty"
                    else:
                        transformed[service_code] = "Is OK"
                else:
                    failed[service_code] = "None"
        elif mongo_ids.get(identifier):
            transformed[identifier] = "Is OK (identifier)"
        else:
            failed[identifier] = "Not found in mongo"

    failed_transform = args.outputdirectory + "failed_transform.json"
    with open(failed_transform, 'w', encoding="utf-8") as failed_file:
        json.dump(failed, failed_file, ensure_ascii=False, indent=4)
    return transformed


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "informationmodels.json"
inputfileNameEnh = args.outputdirectory + "informationmodels_enh.json"
inputfileNameMongo = args.outputdirectory + "mongo_infmodels_id.json"
outputfileName = args.outputdirectory + "informationmodels_transformed.json"


# Transform the organization object to publisher format:
with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, inputfileNameEnh, inputfileNameMongo), outfile, ensure_ascii=False, indent=4)
