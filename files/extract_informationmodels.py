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

dict_list = list(db.informationModelMeta.find(["isPartOf:/abd4d5cd-febe-3e08-ab97-35070fa3d7e9"]))
inf_models = {}
for id_dict in dict_list:
    id_str = id_dict["_id"]
    inf_models[id_str] = id_dict
print("Total number of extracted informationmodels: " + str(len(inf_models)))

with open(args.outputdirectory + 'infmodelsMeta.json', 'w', encoding="utf-8") as outfile:
    json.dump(inf_models, outfile, ensure_ascii=False, indent=4)
