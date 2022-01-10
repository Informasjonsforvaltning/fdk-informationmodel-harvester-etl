import json
import os
import argparse
import fdk_rdf_parser
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
reasoning_uri = os.environ['FDK_BASE_URI'] + '/reasoning/data-services'
headers = {"Accept": "text/turtle"}


dataservice_rdf = requests.get(reasoning_uri, headers=headers).text
dataservices = fdk_rdf_parser.parse_data_services(dataservice_rdf)

filtered = {}
for service in dataservices:
    filtered[dataservices[service].endpointDescription] = service
print("Total number of dataservices: " + str(len(dataservices)))
print("Total number of extracted dataservices: " + str(len(filtered)))

with open(args.outputdirectory + 'dataservices.json', 'w', encoding="utf-8") as outfile:
    json.dump(filtered, outfile, ensure_ascii=False, indent=4)
