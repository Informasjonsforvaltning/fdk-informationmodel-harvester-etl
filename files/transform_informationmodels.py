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
    print(mongo_ids)

    array = info_models["hits"]["hits"]
    array_enh = info_models_enh["hits"]["hits"]

    print(len(array))
    transformed = {}
    failed = {}
    for information_model in array:
        uri = information_model["_source"].get("harvestSourceUri")
        service_code_list = re.findall('schemas(\\d+)', uri)
        if len(service_code_list) == 0 or len(service_code_list) > 1:
            failed[uri] = "Regex failed"
        else:
            service_code = service_code_list[0]
            mongo_data = mongo_ids.get(service_code)
            if mongo_data:
                if len(mongo_data) > 1:
                    failed[service_code] = "Too many hits"
                elif len(mongo_data) == 0:
                    failed[service_code] = "Empty"
                else:
                    transformed[service_code] = "Is OK"
            else:
                failed[service_code] = "None"

    for information_model in array_enh:
        uri = information_model["_source"].get("harvestSourceUri")
        service_code_list = re.findall('schemas(\\d+)', uri)
        if len(service_code_list) == 0 or len(service_code_list) > 1:
            failed[uri] = "Regex failed"
        else:
            service_code = service_code_list[0]
            mongo_data = mongo_ids.get(service_code)
            if mongo_data:
                if len(mongo_data) > 1:
                    failed[service_code] = "Too many hits"
                elif len(mongo_data) == 0:
                    failed[service_code] = "Empty"
                else:
                    transformed[service_code] = "Is OK"
            else:
                failed[service_code] = "None"
    failed_transform = args.outputdirectory + "failed_transform.json"
    with open(failed_transform, 'w', encoding="utf-8") as failed_file:
        json.dump(failed, failed_file, ensure_ascii=False, indent=4)
    return transformed

    # if informationmodel["_source"].get("serviceType") != "Kontoopplysninger" and dataservice["_source"].get("apiSpecUrl"):
    #     first = dataservice["_source"].get("harvest")["firstHarvested"]
    #     dataservice2 = {"doc": {"id": dataservice["_id"],
    #                             "harvest": {"firstHarvested": first,
    #                                         "lastHarvested": dataservice["_source"].get("harvest")["lastHarvested"],
    #                                         "changed": mapchanged(dataservice["_source"].get("harvest"), first)
    #                                         }
    #                             }
    #                     }
    #     transformed[dataservice["_source"].get("apiSpecUrl")] = dataservice2
    # print("Total to be transformed: ", len(transformed))
    # return transformed


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
