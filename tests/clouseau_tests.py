from nose.tools import *
from clouseau.clouseau import Parser, Node, Clouseau



def clouseau_should_fetch_git_repo_test():
    """
    If repr doesn't exist, clone, it exists, pull
    """
    




def clouseau_should_parse_args_test():
    args = ['-u', 'git@github.com/foo/baz.git']
    parsed = clouseau.parse_args( args )
    eq_( 'baz.git', parsed['repo'] )
    eq_( 'temp/baz', parsed['repo_dir'] )
    eq_( 'baz', parsed['repo_name'] )
    #ok_(False, "Needed to see how to test this. Failing intentionally because it needs work.")




def parser_test():
    parser = Parser()



def smoke_test():
    """
    Simple smoke test
    """
    #print "I am what I am and I am passing"
    parser = Parser()
    node = Node('function','foo bar baz', None)
    clouseau = Clouseau()
    ok_(True)



def setUp():
    global clouseau 
    clouseau = Clouseau()

def tearDown():
    pass

