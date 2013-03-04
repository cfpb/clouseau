import os
from nose.tools import *
from clouseau.clouseau import Parser, Node, Clouseau
from clouseau.colors import *
from jinja2 import Template, Environment, PackageLoader



def jinja_test():
    terms = [ 'password', 'gov']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    #Requires Cato to be present
    clouseau.render_to_console( terms, parsed )





def template_2_console_test():
    p = Parser()
    terms = ['password']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    ids = p.parse(terms, parsed['repo_dir'] )
    template = Template( "Hello, {{you}}." )
    print template.render(you= cyan("honey bunny"))




def parser_should_build_data_structure_for_each_term_test():
    p = Parser()
    terms = ['password']
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    print darkcyan( parsed )
    ids = p.parse(terms, parsed['repo_dir'] )
    print cyan( ids )




def clouseau_should_fetch_git_repo_test():
    """
    If repr doesn't exist, clone, it exists, pull
    """
    args = ['-u', 'git://github.com/virtix/cato.git']
    parsed = clouseau.parse_args( args )
    results = clouseau.clone_repo( parsed['url'], parsed['repo_dir'] )
    ok_(results)

    




def clouseau_should_parse_args_test():
    args = ['-u', 'git@github.com/foo/baz.git']
    parsed = clouseau.parse_args( args )
    #print parsed
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
    path = os.path.abspath( __file__ )
    cwd = os.path.dirname( path )
    os.chdir( cwd )

