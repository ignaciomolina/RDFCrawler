# RDFCrawler
This repository contains a Python module with the following services:
  - __rdf_crawler__: Crawler that explores from a root URI all endpoint objects refered in RDF's predicates.
  - __rdf_service__: Deploys a RESTFul service that replicates all the URIs gathered by the crawler.
    - Endpoints:
      - RDF: Service offers the replicated object's predicates.
      - Update: Service also has an endpoint to update crawling information.
    - Configuration: URI has to be set in rdf_crawler.cfg
