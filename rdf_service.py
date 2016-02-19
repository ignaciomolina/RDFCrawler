import re
from datetime import datetime

from flask import Flask, make_response, request
from rdflib import URIRef

from rdf_crawler import RDFCrawler

__author__ = 'Ignacio Molina Cuquerella'
__email__ = 'imolina@centeropenmiddleware.com'


app = Flask(__name__)


@app.route('/update', methods=['POST'])
def update_graph():

    crawler.start()

    return make_response('Crawling complete after: %s seconds with %s '
                         'predicates.' % (crawler.last_process_time,
                                          len(crawler.graph)), 200)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>')
def get_resource(path):

    target = '%s%s' % (crawler.root, path)

    graph = crawler.graph.get_context(URIRef(target))

    if len(graph) == 0:
        return make_response('No endpoint found at %s' % request.url, 404)

    date = datetime.utcfromtimestamp(crawler.last_update)\
        .strftime('%a, %d %b %Y %H:%M:%S %Z')

    return make_response(graph.serialize(base='http://localhost:5000/',
                                         format='turtle')
                         .replace(crawler.root, 'http://localhost:5000/'), 200,
                         {'Content-Type': 'text/turtle',
                          'Last-Modified': '%s GMT' % date})


if __name__ == '__main__':

    # Read configuration file
    f = open('rdf_crawler.cfg', 'r')
    config = f.read()
    m = re.search("root = '(.*)'", config)
    f.close()

    if m is not None:
        root_uri = m.group(1)
        crawler = RDFCrawler(root_uri)
        crawler.start()

        app.run()

    else:
        print('No URI has been set it.')
        exit(0)
