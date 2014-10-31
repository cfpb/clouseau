#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Clouseau, a silly git repo inspector
#
#
import os
import argparse as arse
import pprint
import sys
import subprocess
from clients import *
from clients.colors import *
from parser import Parser
from commit_parser import CommitParser
from terms_collector import TermsCollector
from clouseau_model import ClouseauModel


VERSION='0.2.0'

class Clouseau:
    """
    Wrap and delegate
    """
    

    def __init__(self):
        pass


    def main(self , _args, client):
        
        args = self.parse_args( _args )

        collector = TermsCollector()
        terms = collector.collect_terms( args['patterns'], args['term'] )
        model = ClouseauModel(args['github_url'], terms)

        # Clone repo
        if(not args['skip']):
            self.clone_repo( args['url'], args['repo_dir'] ) 
        else:
            print blue( 'Skipping git-clone or git-pull as --skip was found on the command line.' )

        if args['revlist'] != None and args['revlist'] != 'all':
            parser = CommitParser()
            parser.parse(terms=terms, repo=args['repo_dir'], revlist=args['revlist'], clouseau_model=model, github_url=args['github_url'])
            results = model.model
        else:
            parser = Parser()
            results = parser.parse( terms=terms, repo=args['repo_dir'], revlist=args['revlist'] ,
                    before=args['before'], after=args['after'], author=args['author'], github_url=args['github_url'])

        # pprint.pprint(results)
        client.render( terms, results )


    def clone_repo(self, url, destination):
        try:
            _out = subprocess.check_output(['git', 'clone', url, destination])        
        
        except subprocess.CalledProcessError:
            print blue( "Directory, %s, exits. Trying git-pull instead of clone." % destination )
            _out = subprocess.check_output(['git', '--git-dir=%s/.git' % destination, 'pull'])       
            print smoke( "Git says: %s" % _out )
            return _out
        
        except :
            e = sys.exc_info()[0]
            print red( 'Problem writing to destination: %s' % destination ) 
            raise
        
        return _out
            


    # Belongs in console client
    def parse_args( self, arguments ):
        
        _dir = os.path.dirname(__file__)
        _default_pattern_file = 'patterns/default.txt'
        _pattern_path = os.path.join( _dir, _default_pattern_file )
        _temp = os.path.join( _dir, "../temp")

        p = arse.ArgumentParser (prog="clouseau", description="  Clouseau: A silly git inspector", version=VERSION)
        p.add_argument('--url', '-u', required=True,  action="store", dest="url",
                        help="The fully qualified git URL (http://www.kernel.org/pub/software/scm/git/docs/git-clone.html)")
        p.add_argument('--term', '-t', required=False, action="store", dest="term",
                        help="Search for a single regular expression instead of every item in patterns/default.txt"),
        p.add_argument('--patterns', '-p', action="store", dest="patterns", default=_pattern_path,
                        help="File path to a list of regular expressions to use. Can be a comma-separated list of files. See patterns/default.txt")
        p.add_argument('--clean', '-c',  dest="clean", action="store_true", default=False,
                        help="Delete the existing git repo and re-clone")
        p.add_argument('--output', '-o', dest="output_format", required=False,
                        help="Output formats: console, markdown, raw, html, json, csv. Default: console.")
        p.add_argument('--output-destination', '-od', dest="output_destination", required=False, default=_temp,
                        help="Location where the output is to be stored. Default clouseau/temp.")
        p.add_argument('--dest', '-d', dest="dest", default=_temp,
                        help="The directory where the git repo is to be stored. Default: clouseau/temp")
        p.add_argument('--revlist', '-rl', required=False, dest="revlist",
                        help="A space-delimted list of revisions (commits) to search. Defaults to HEAD. Specify 'all'" \
                             " to search the entire history.")
        p.add_argument('--before', '-b', dest='before', required=False,
                        help="Search commits that occur prior to this date; e.g., Mar-08-2013")
        p.add_argument('--after', '-a', dest="after", required=False,
                        help="Search commits that occur after this date; e.g., Mar-10-2013")
        p.add_argument('--author', dest="author", required=False,
                        help="Perform searched for commits made by AUTHOR. An email address is fine.")
        p.add_argument('--skip', '-s', dest="skip", action="store_true",
                        help="If specified, skips any calls to git-clone or git-pull. Useful in combination with --dest to test a local git repo")

        args = p.parse_args( arguments )
        url = args.url.rstrip('/')
        github_url = url.rstrip('.git')
        repo = url.rsplit('/',1)[1]
        repo_name = repo.rstrip('.git')
        self.args = args
        return { "url": url,
                 "github_url": github_url ,
                 "repo": repo,
                 "repo_name": repo_name,
                 "repo_dir": ("%s/%s" % (args.dest,repo_name) ),
                 "clean": args.clean,
                 "output_format": args.output_format,
                 "dest": args.dest,
                 "patterns": args.patterns,
                 "revlist": args.revlist,
                 "term": args.term,
                 "before": args.before,
                 "after": args.after,
                 "author": args.author,
                 "skip": args.skip
              }





