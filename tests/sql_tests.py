import os
from nose.tools import *
from clouseau.clouseau import Clouseau
from clouseau.parser import Parser
from clouseau.colors import *
from clouseau.clients.console import ConsoleClient
from jinja2 import Template, Environment, PackageLoader
import pickle
from pprint import pprint
import types



def test_this():
    pass
            
def test_load_pickle():
    f = open('tests/fixtures/cato.pickle')
    c = pickle.load(f)
    pprint (c,width=2)


def test_load_ClouseauDb():
    cdb = ClouseauDb()
    ok_ (isinstance( cdb, types.InstanceType ) , "Make sure you're returning an object.")
    eq_ ( cdb.__class__, ClouseauDb , "Changed class name or location?")


def test_clouseau_db_config():
    cdb = ClouseauDb( db_name='foo_db.sqlite' )
    eq_ ( 'foo_db.sqlite', cdb.db.split( os.sep )[-1] )


def test_sqlite_db_is_present():
    import sqlite3
    cdb = ClouseauDb()


def test_load_MatchedClouseauObject():
    # 
    o = MatchedClouseauObject()
    #print type(o.__class__)

# ----------------------------------------------------------------------

class ClouseauDb():
    import os
    import sqlite3

    """
    Should control the db connection data: location, credentials, etc
    """
    
    def __init__(self, db_name='clouseaudb.sqlite'):
        _dir = os.path.dirname( __file__ )
        # Assumes this class's module is a sibling og .clouseau
        self.db = os.path.join( _dir, '../.clouseau/%s' % db_name )
        # Oh, Python, you self-ish thing.
        self.conn =  self.sqlite3.connect( self.db )




class MatchedClouseauObject( ClouseauDb ):
    """
    fields = (term, refspec, src, git_log_id, matched_lines_id )
    fk = ( GitLog, MatchedLines )
    GitLog = ( commit_id - fk^matchedclouseauinstance, author, date, message  )
    MatchedLines = ( commit_id - fk^matchedclouseauinstance, line_number, line_text )
    
    """

    pass

