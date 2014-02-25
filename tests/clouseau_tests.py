import os, pprint
from nose.tools import *
from clouseau.clouseau import Clouseau
from clouseau.parser import Parser
from clouseau.commit_parser import CommitParser
from clouseau.terms_collector import TermsCollector
from clouseau.clouseau_model import ClouseauModel
from clouseau.clients.colors import *
from clouseau.clients.console import ConsoleClient
from jinja2 import Template, Environment, PackageLoader



def search_test():
    ok_(False, "Fix me")


def generate_revlist_test():
    ok_(False , "Fix me")


def parser_should_build_data_structure_for_each_term_test():
    p = Parser()
    terms = ['password']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    #print smoke( parsed )
    ids = p.parse(terms, parsed['repo_dir'] )
    eq_(2, len(ids) , "This should have 2 keys: term (password) and meta" )



def clouseau_should_parse_args_test():
    args = ['-u', 'git@github.com/foo/baz.git']
    parsed = clouseau.parse_args( args )
    eq_ ('git@github.com/foo/baz', parsed['github_url'] )
    eq_( 'baz.git', parsed['repo'] )


def pattern_parser_test():
    parser = Parser()
    patterns = open( 'clouseau/patterns/default.txt', 'r' )
    terms = parser.parse_terms( patterns_file=patterns, single_term=None )
    ok_( len(terms) > 5 )

def commit_parser_test():
    parser = CommitParser()
    patterns = open( 'clouseau/patterns/default.txt', 'r' )
    commit_output = open('tests/fixtures/commit_show.txt', 'r')

    holder = {}
    terms = TermsCollector().collect_terms('clouseau/patterns/default.txt', None)
    model = ClouseauModel('https://github.com/virtix/clouseau', terms)
    parser.parse_commit(terms, commit_output.read(), holder, model)
    print "holder is "
    pprint.pprint(holder)

    print "clouseau model is "
    pprint.pprint(model.model)

def diff_header_to_filenames_test():
    parser = CommitParser()
    (left, right) = parser.diff_header_to_file_names("a/hooktest2.txt b/hooktest2.txt")
    eq_("hooktest2.txt", left)
    eq_("hooktest2.txt", right)

    (left, right) = parser.diff_header_to_file_names("a/somedir/hooktest2.txt b/somedir/hooktest2.txt")
    eq_("somedir/hooktest2.txt", left)
    eq_("somedir/hooktest2.txt", right)

# Fetched some pre-generated data
def get_results():
    import pickle
    data = open( 'tests/fixtures/cato.pickle', 'r' )
    ids = pickle.load( data ) 
    eq_(2, len(ids) , "This guard condition should have 2 keys: term (password) and meta" )
    return ids



def smoke_test():
    """
    Simple smoke test
    """
    #print "I am what I am and I am passing"
    parser = Parser()
    clouseau = Clouseau()
    ok_(True)



def setUp():
    global clouseau 
    clouseau = Clouseau()

def tearDown():
    path = os.path.abspath( __file__ )
    cwd = os.path.dirname( path )
    os.chdir( cwd )

