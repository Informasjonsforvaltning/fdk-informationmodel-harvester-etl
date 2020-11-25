import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform(extract):
    # Transforming according to rules in README
    array = extract["hits"]["hits"]
    print(len(array))
    transformed = {}
    for dataservice in array:
        if dataservice["_source"].get("serviceType") != "Kontoopplysninger" and dataservice["_source"].get("apiSpecUrl"):
            first = dataservice["_source"].get("harvest")["firstHarvested"]
            dataservice2 = {"doc": {"id": dataservice["_id"],
                                    "harvest": {"firstHarvested": first,
                                                "lastHarvested": dataservice["_source"].get("harvest")["lastHarvested"],
                                                "changed": mapchanged(dataservice["_source"].get("harvest"), first)
                                                }
                                    }
                            }
            transformed[dataservice["_source"].get("apiSpecUrl")] = dataservice2
    print("Total to be transformed: ", len(transformed))
    return transformed


def mapchanged(harvest, first):
    array = harvest.get("changed") if harvest.get("changed") else []
    if len(array) > 0:
        return array
    else:
        array.append(first)
        return array


inputfileName = args.outputdirectory + "dataservices.json"
outputfileName = args.outputdirectory + "dataservices_metadata.json"
with open(inputfileName) as json_file:
    data = json.load(json_file)
    # Transform the organization object to publihser format:
    with open(outputfileName, 'w', encoding="utf-8") as outfile:
        json.dump(transform(data), outfile, ensure_ascii=False, indent=4)
