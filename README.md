# RDFCrawler
This repository contains a Python module with the following services:
  - __rdf_crawler__: Crawler that explores from a linked data domain all resources refered in RDF's triplets.
  - __rdf_service__: Deploys a RESTFul service that replicates all the URIs gathered by the crawler.
    - Endpoints:
      - /{resource-identifier}/: Service offers the replicated object's triplets.
      - /Update: Service also has an endpoint to update crawling information.
      - /stats: Shows information about the linked data crawled
        - list of entities used in domain
        - num of entities
        - update date
        - processing time
        - source domain
        - disk usage

Release:
  -  This project has been release in Pypi repository under the name 'RDFCrawler'
  -  Also exists a Docker Image in https://hub.docker.com/r/ignaciomolina/docker-rdfcrawler/
