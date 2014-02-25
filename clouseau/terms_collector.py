import os
import sys


# -----------------------------------------------------------------------------------------------
class TermsCollector:
    """
    Collects all search terms from the patterns files
    """

    def __init__( self ):
        pass

    def collect_terms( self, patterns_files, single_term ):
        terms = []
        for f in patterns_files.split(","):
            with open(f) as pf:
                [terms.append(line) for line in pf.readlines()]

        if( single_term != None ):
            terms = { single_term }
        terms = [term.strip() for term in terms if not term.startswith('#') and term.strip() != '']

        return terms