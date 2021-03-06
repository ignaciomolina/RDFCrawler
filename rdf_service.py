import json
import logging
import os, time
import sys
from datetime import datetime
from threading import Thread

from flask import Flask, make_response, request
from rdflib import URIRef, RDF

from rdf_crawler import RDFCrawler

__author__ = 'Ignacio Molina Cuquerella'
__email__ = 'imolina@centeropenmiddleware.com'


app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/update', methods=['POST'])
def update_graph():

    if not crawler.lock.acquire(False):
        return make_response('Crawling in progress.', 503)

    Thread(target=crawler.start).start()

    crawler.lock.release()
    return make_response('Initiated crawling exploration for %s' % crawler.root,
                         200, {'Content-Type': 'text/plain'})


@app.route('/stats', methods=['GET'])
def get_stats():

    date = get_last_update(crawler.graph_route)

    entities = get_contexts(crawler.graph)

    size = dict()
    size['size'] = get_size(crawler.graph_route)
    size['measure'] = 'MB'

    response = dict()
    response['source'] = crawler.root
    response['num_entities'] = str(len(entities))
    response['num_triplets'] = str(len(crawler.graph))
    response['entities'] = entities
    response['size'] = size
    response['crawling_time'] = crawler.last_process_time
    response['last_update'] = date

    return make_response(json.dumps(response), 200,
                         {'Content-Type': 'application/json'})


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>')
def get_resource(path):

    negotiation = request.headers.get("Accept", "text/turtle")
    if 'text/turtle' not in negotiation and '*/*' not in negotiation:
        return make_response('', 406)

    target = '%s%s' % (crawler.root, path)

    graph = crawler.graph.get_context(URIRef(target))

    if len(graph) == 0:
        return make_response('No endpoint found at %s' % request.url, 404)

    date = get_last_update(crawler.graph_route)

    header = dict()
    header['Content-Type'] = 'text/turtle'
    header['Last-Modified'] = '%s GMT' % date,
    header['ETag'] = '%s' % hash(date)

    return make_response(graph.serialize(base=request.url_root,
                                         format='turtle')
                         .replace(crawler.root, request.url_root), 200, header)


def get_contexts(graph):

    entities = dict()

    for s in graph.subjects():
        for o in graph.objects(s, RDF.type):
            entities[o] = entities.get(o, 0) + 1

    return entities


def get_last_update(folder):

    last_update = os.path.getmtime(folder)

    date = datetime.utcfromtimestamp(last_update)\
        .strftime('%a, %d %b %Y %H:%M:%S %Z')

    return date


def get_size(folder):

    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            total_size += os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            total_size += get_size(item_path)
    return total_size / 1024.0 / 1024.0

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) == 2:

        root_uri = sys.argv[1]
        crawler = RDFCrawler(root_uri)
        app.run(host='0.0.0.0',
                threaded=True)

    else:
        print('rdf_service.py <uri>')
        exit(0)
