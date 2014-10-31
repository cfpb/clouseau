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



def clouseau_should_parse_args_test():
    args = ['-u', 'git@github.com/foo/baz.git']
    parsed = clouseau.parse_args( args )
    eq_ ('git@github.com/foo/baz', parsed['github_url'] )
    eq_( 'baz.git', parsed['repo'] )


def collect_terms_test():
    terms = TermsCollector().collect_terms('clouseau/patterns/default.txt', None)
    ok_( len(terms) > 5 )

def commit_parser_test():
    parser = CommitParser()
    commit_output = open('tests/fixtures/commit_show.txt', 'r')

    terms = TermsCollector().collect_terms('clouseau/patterns/default.txt', None)
    model = ClouseauModel('https://github.com/cfpb/clouseau', terms)
    parser.parse_commit(terms, commit_output.read(), model)

    ### Brittleness alert: These tests are based on the fixture file. The assertions are quite specific, based on what we know to be true about the fixture
    # print "clouseau model is "
    # print model
    ip_pattern = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    eq_(4, len(model.model[ip_pattern]))
    eq_(8, model.model[ip_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:somedir_hooktest2_txt']['matched_lines'][0][0])
    eq_(7, model.model[ip_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:hooktest_txt']['matched_lines'][0][0])
    eq_('+My IP is 127.0.0.5', model.model[ip_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:hooktest_txt']['matched_lines'][0][1])

    pass_equals_pattern = "password[ ]*=[ ]*.+"
    eq_(2, len(model.model[pass_equals_pattern]))
    eq_(1, model.model[pass_equals_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:Commit_Message']['matched_lines'][0][0])
    eq_('Commit Message', model.model[pass_equals_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:Commit_Message']['src'])
    eq_(3, model.model[pass_equals_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:somedir_hooktest2_txt']['matched_lines'][0][0])
    eq_(4, model.model[pass_equals_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:somedir_hooktest2_txt']['matched_lines'][1][0])
    eq_(5, model.model[pass_equals_pattern]['d1859009afc7e48506ec025a07f4f90ce4c5a210:somedir_hooktest2_txt']['matched_lines'][2][0])

def commit_parser_merge_only_test():
    parser = CommitParser()
    commit_output = open('tests/fixtures/commit_show_merge_only.txt', 'r')

    terms = TermsCollector().collect_terms('clouseau/patterns/default.txt', None)
    model = ClouseauModel('https://github.com/cfpb/clouseau', terms)
    parser.parse_commit(terms, commit_output.read(), model)
    exec_in_commit = model.model['exec'].keys()[0]
    eq_(1, model.model['exec'][exec_in_commit]['matched_lines'][0][0])
    eq_('Commit Message', model.model['exec'][exec_in_commit]['src'])

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

