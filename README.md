# RDFCrawler
This repository contains a Python module with the following services:
  - __rdfcrawler__: Crawler that explores from a root URI all endpoint objects refered in RDF's predicates.
  - __rdfservice__: Deploys a RESTFul service that replicates all the URIs gathered by the crawler.
    - Endpoints:
      - RDF: Service offers the replicated object's predicates.
      - Update: Service also has an endpoint to update crawling information.
    - Configuration: URI has to be set in RDFCrawler.cfg
