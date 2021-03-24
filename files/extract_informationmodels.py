import json
import os
import re
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/informationModelHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.informationModelHarvester

namespace = os.environ['NAMESPACE']

staging_catalogs = [{"_id": "https://www.altinn.no/models/altinn", "fdkId": "f27930d7-8070-3d12-b4c7-e6aae22a478f"},
                    {"_id": "https://www.altinn.no/models/or", "fdkId": "73925a02-21a0-3ad9-948c-ac017299ec22"},
                    {"_id": "https://www.altinn.no/models/seres", "fdkId": "c62b1bd8-17a1-3724-9d00-db020a2025b8"}]
other_catalogs = [{"_id": "https://www.altinn.no/models/catalog", "fdkId": "30251da7-e78f-33e5-9249-375451c9b187"}]


def get_part_of_uri(fdkId):
    if namespace == "staging":
        return f"https://informationmodels.staging.fellesdatakatalog.digdir.no/catalogs/{fdkId}"
    elif namespace == "demo":
        return f"https://informationmodels.demo.fellesdatakatalog.digdir.no/catalogs/{fdkId}"
    else:
        return f"https://informationmodels.fellesdatakatalog.digdir.no/catalogs/{fdkId}"


if namespace == "staging":
    catalogs = staging_catalogs
else:
    catalogs = other_catalogs

infModelMeta_list = []
for catalog in staging_catalogs:
    staging_fdkId = catalog["fdkId"]
    uri = get_part_of_uri(staging_fdkId)
    infModelMeta_list.extend(list(db.informationmodelMeta.find({"isPartOf": f"{uri}"}, {"fdkId": 1})))

with open(args.outputdirectory + 'infmodelsMeta.json', 'w', encoding="utf-8") as outfile:
    json.dump(infModelMeta_list, outfile, ensure_ascii=False, indent=4)
