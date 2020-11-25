import json
import requests
import os

import argparse

from rdflib import Graph, URIRef, Literal, XSD
from rdflib.namespace import FOAF, RDF, DCTERMS
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

fuseki_extract = args.outputdirectory + "dataservices.ttl"

dataservicesGraph = None
with open(fuseki_extract) as fuseki_file:
    dataservicesGraph = Graph().parse(data=fuseki_file.read(), format='turtle')
metabaseURI = os.environ['DATASERVICE_HARVESTER_BASE_URI'] + '/dataservices/'
catalogrecordRef = URIRef("http://www.w3.org/ns/dcat#CatalogRecord")
fusekibaseURI = 'http://fdk-fuseki-service:8080/fuseki/dataservice-meta'

inputfileName = args.outputdirectory + "dataservices_metadata.json"

with open(inputfileName) as json_file:

    data = json.load(json_file)
    # Load the publisher by posting the data:
    totalLoaded = 0
    totalFailed = 0

    for recordURI in dataservicesGraph.subjects(
            predicate=RDF.type, object=catalogrecordRef
    ):
        primaryTopicURI = dataservicesGraph.value(recordURI, FOAF.primaryTopic)
        endpointDescription = dataservicesGraph.value(primaryTopicURI, URIRef("http://www.w3.org/ns/dcat#endpointDescription"))
        if endpointDescription:
            elastic_dataservice = data.get(endpointDescription.toPython())
            if elastic_dataservice:
                elasticID = elastic_dataservice["doc"]["id"]
                elasticFirst = elastic_dataservice["doc"]["harvest"]["firstHarvested"]
                elasticChanged = elastic_dataservice["doc"]["harvest"]["changed"]

                g = Graph()
                resourceURI = URIRef(metabaseURI + elasticID)
                partOfURI = dataservicesGraph.value(recordURI, DCTERMS.isPartOf)
                g.resource(resourceURI)
                g.add((resourceURI, RDF.type, catalogrecordRef))
                g.add((resourceURI, DCTERMS.identifier, Literal(elasticID)))
                g.add((resourceURI, DCTERMS.isPartOf, partOfURI))
                g.add((resourceURI, DCTERMS.issued, Literal(elasticFirst, datatype=XSD.dateTime)))
                for date in elasticChanged:
                    g.add((resourceURI, DCTERMS.modified, Literal(date, datatype=XSD.dateTime)))
                g.add((resourceURI, FOAF.primaryTopic, primaryTopicURI))
                old_identifier = dataservicesGraph.value(recordURI, DCTERMS.identifier)

                try:
                    response = requests.put(
                        fusekibaseURI + '?graph=' + elasticID, data=g.serialize(), headers={"Content-type": "application/rdf+xml"}
                    )
                    response.raise_for_status()
                    print("Response.status: " + str(response.status_code) + " -- " + endpointDescription.toPython())
                    if response.status_code == "201":
                        totalLoaded += 1
                        try:
                            response = requests.delete(
                                fusekibaseURI + '?graph=' + old_identifier
                            )
                            response.raise_for_status()
                            print("Delete response.status: " + str(response.status_code) + " -- " + endpointDescription.toPython())
                        except requests.HTTPError as err:
                            logging.error(f'Http delete error response from reference-data: ({err})')
                        except Exception as err:
                            logging.error(f"Error occured when deleting data from reference-data: ({err})")
                except requests.HTTPError as err:
                    logging.error(f"Http error response from reference-data: ({err})")
                except Exception as err:
                    logging.error(f"Error occured when getting data from reference-data: ({err})")
