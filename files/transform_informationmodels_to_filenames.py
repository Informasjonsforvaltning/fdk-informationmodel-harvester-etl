import json
import re
import argparse
from datetime import datetime
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
namespace = os.environ['NAMESPACE']
harvest_filenames_staging = ["https://altinn-model-publisher.staging.fellesdatakatalog.digdir.no/altinn",
                             "https://altinn-model-publisher.staging.fellesdatakatalog.digdir.no/or",
                             "https://altinn-model-publisher.staging.fellesdatakatalog.digdir.no/seres"]
harvest_filenames_demo = ["https://altinn-model-publisher.demo.fellesdatakatalog.digdir.no/models"]
harvest_filenames_prod = ["https://altinn-model-publisher.digdir.no/models"]
staging_catalogs = [{"_id": "https://www.altinn.no/models/altinn", "fdkId": "f27930d7-8070-3d12-b4c7-e6aae22a478f"},
                    {"_id": "https://www.altinn.no/models/or", "fdkId": "73925a02-21a0-3ad9-948c-ac017299ec22"},
                    {"_id": "https://www.altinn.no/models/seres", "fdkId": "c62b1bd8-17a1-3724-9d00-db020a2025b8"}]
other_catalogs = [{"_id": "https://www.altinn.no/models/catalog", "fdkId": "30251da7-e78f-33e5-9249-375451c9b187"}]
if namespace == "staging":
    catalogs = staging_catalogs
else:
    catalogs = other_catalogs


def transform(inputfile):
    info_models = openfile(inputfile)
    if namespace == "staging":
        transformed = harvest_filenames_staging
    elif namespace == "demo":
        transformed = harvest_filenames_demo
    else:
        transformed = harvest_filenames_prod

    for catalog in catalogs:
        transformed.extend(catalog_filenames(catalog["fdkId"]))
    for model in info_models:
        transformed.extend(informationmodel_filenames(model["fdkId"]))

    return transformed


def catalog_filenames(fdkId):
    return [f'catalog-{fdkId}', f'catalog-no-records-{fdkId}']


def informationmodel_filenames(fdkId):
    return [f'informationmodel-{fdkId}', f'informationmodel-no-records-{fdkId}']


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "infmodelsMeta.json"
outputfileName = args.outputdirectory + "filenames.json"


# Transform the organization object to publisher format:
with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)
