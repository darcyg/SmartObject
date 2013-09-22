'''
Created on Sep 21, 2013

LinkFormatProxy provides a Core Link-Format interface to a SmartObject Description. 
The Link-Format Interface provides a subset of the relations found in the description
based on bindings of Link-Format attributes to RDF Predicates

@author: mjkoster
'''

from RESTfulResource import RESTfulResource
from rdflib.graph import Graph
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL
from Observers import Observers

 
class LinkFormatProxy (RESTfulResource):
    
    def __init__(self, parentObject=None, resourceName=''):
        RESTfulResource.__init__(self, parentObject, resourceName)
        # make a reference to the graph inside the associated Description resource
        self.graph = self.resources['parentObject'].resources['parentObject'].Description.graph
        # This resource supports link-format only
        self._parseContentTypes = [ 'application/link-format' ]
        self._serializeContentTypes = [ 'application/link-format' ]
        self.fmt = { 'application/link-format': 'linkFormat' }
        
        # attribute - predicate bindings RDF - core-link-format
        self._attrToPred = {'"rt"': RDFS.Resource,
                            '"if"': RDF.type }
        
        self._predToAttr = {RDFS.Resource: '"rt"',
                            RDF.type: '"if"' }


    def get(self, query=None):
        # return a sub-graph consisting of the triples with predicates in the attribute binding
        # filtered by the query 
        g = Graph()
        for self._pred in self._predToAttr:
            for triple in self.graph.triples((None, self._pred, None)) :
                g.add(triple)
        print g.triples()
        return g
    
    def set(self, newGraph):
        # update description graph with new subgraph
        self.graph += newGraph
        
    # exposed methods for converting sub graphs to and from specified representation
    def parse(self, source, cType):
        # assume format = link-format
        g = Graph()
        self._linkFormatString = source
        self._graphs = self._linkFormatString.split(',')
        for self._graph in self._graphs:
            self._subject, self._links = self._graph.split(';')
            self._subject = self._subject.strip('<')
            self._subject = self._subject.strip('>')
            for self._link in self._links:
                self._attr, self._objs = self._link.split('=')
                self._objs = self.objs._split(' ')
                for self._obj in self._objs:
                    g.add( URIRef(self._subject), self._attrToPred[self._attr], self._obj )            
        return g 
    
    def serialize(self, graph, cType): 
        # assume format = link-format
        self._linkFormatString = ''
        for self._subj in graph.subjects(None, None):
            self._linkFormatString += '<' + str(self._subj) + '>'
            for self._pred in graph.predicates(self._subj, None):
                self._linkFormatString += ';' + self._predToAttr[self._pred] + '='
                for self._obj in graph.objects(self._subj, self._pred):
                    self._linkFormatString += self._obj + ' '
            self._linkFormatString += ',' # is the trailing space in values and trailing comma here OK?
            print self._linkFormatString
        return self._linkFormatString
       
    def serializeContentTypes(self) :
        return self._serializeContentTypes
    
    def parseContentTypes(self) :
        return self._parseContentTypes
    
        