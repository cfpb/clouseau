import os
from nose.tools import *
from clouseau.clouseau import Clouseau
from clouseau.parser import Parser
from clouseau.clients.colors import *
from clouseau.clients.console_thin import ConsoleThinClient
from jinja2 import Template, Environment, PackageLoader




# Integration test
def console_client_test():
    parser = Parser()
    terms = ['password']
    args = ['-u', 'https://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    print parsed
    ids = parser.parse( terms=terms, repo=parsed['repo_dir'], revlist=parsed['revlist'],
                        before=parsed['before'], after=parsed['after'], author=parsed['author'],
                        github_url=parsed['github_url'])

    #ids = p.parse(terms, parsed['repo_dir'] )
    #print ids
    client = ConsoleThinClient()
    client.render( terms, ids )


#integration test
def parser_should_build_data_structure_for_each_term_test():
    """
    If repr doesn't exist, clone; if exists, pull
    Ensure appropriate data structure built for search terms
    """
    p = Parser()
    terms = ['password']
    args = ['-u', 'https://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    clouseau.clone_repo( parsed['url'], parsed['repo_dir'] )

    ids = p.parse(terms, parsed['repo_dir'] )
    eq_(2, len(ids) , "This should have 2 keys: term (password) and meta" )


def setUp():
    global clouseau 
    clouseau = Clouseau()

def tearDown():
    path = os.path.abspath( __file__ )
    cwd = os.path.dirname( path )
    os.chdir( cwd )

