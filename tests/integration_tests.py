import os
from nose.tools import *
from clouseau.clouseau import Clouseau
from clouseau.parser import Parser
from clouseau.colors import *
from clouseau.clients.console import ConsoleClient
from jinja2 import Template, Environment, PackageLoader




# Integration test
def console_client_test():
    parser = Parser()
    terms = ['password']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    ids = parser.parse( terms=terms, repo=parsed['repo_dir'], pathspec=parsed['pathspec'], 
                        before=parsed['before'], after=parsed['after'], author=parsed['author'], 
                        github_url=parsed['github_url'],skip=True)
        
    #ids = p.parse(terms, parsed['repo_dir'] )
    #print ids
    client = ConsoleClient()
    client.render( terms, ids )




#integration test
def parser_should_build_data_structure_for_each_term_test():
    p = Parser()
    terms = ['password']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    #print smoke( parsed )
    ids = p.parse(terms, parsed['repo_dir'] )
    eq_(2, len(ids) , "This should have 2 keys: term (password) and meta" )



#integration test
def clouseau_should_fetch_git_repo_test():
    """
    If repr doesn't exist, clone, it exists, pull
    """
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    results = clouseau.clone_repo( parsed['url'], parsed['repo_dir'] )
    ok_(results)

    


def setUp():
    global clouseau 
    clouseau = Clouseau()

def tearDown():
    path = os.path.abspath( __file__ )
    cwd = os.path.dirname( path )
    os.chdir( cwd )

