import re
import sys
from datetime import datetime

from flask import Flask, make_response, request
from rdflib import URIRef

from rdf_crawler import RDFCrawler

__author__ = 'Ignacio Molina Cuquerella'
__email__ = 'imolina@centeropenmiddleware.com'


app = Flask(__name__)


@app.route('/update', methods=['POST'])
def update_graph():

    if not crawler.lock.acquire(False):
        return make_response('Crawling in progress.', 503)

    crawler.start()

    crawler.lock.release()
    return make_response('Crawling complete after: %s seconds with %s '
                         'predicates.' % (crawler.last_process_time,
                                          len(crawler.graph)), 200)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>')
def get_resource(path):

    if not crawler.lock.acquire(False):
        return make_response('Service currently busy with update process.', 503)

    target = '%s%s' % (crawler.root, path)

    graph = crawler.graph.get_context(URIRef(target))

    if len(graph) == 0:
        return make_response('No endpoint found at %s' % request.url, 404)

    date = datetime.utcfromtimestamp(crawler.last_update)\
        .strftime('%a, %d %b %Y %H:%M:%S %Z')

    crawler.lock.release()
    return make_response(graph.serialize(base=request.url_root,
                                         format='turtle')
                         .replace(crawler.root, request.url_root), 200,
                         {'Content-Type': 'text/turtle',
                          'Last-Modified': '%s GMT' % date,
                          'ETag': '%s' % hash(date)})


if __name__ == '__main__':

    if len(sys.argv) == 2:

        root_uri = sys.argv[1]
        crawler = RDFCrawler(root_uri)
        app.run(host='0.0.0.0',
                threaded=True)

    else:
        print('rdf_service.py <uri>')
        exit(0)
