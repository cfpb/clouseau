#! /usr/bin/ENV python
# -*- coding: utf-8 -*-
#
# Clouseau, a silly git repo inspector
#
#
import os
import shutil
import subprocess
import logging
import re
import json
import pprint
import argparse as arse
import textwrap
from output import *

pp = pprint.PrettyPrinter()

VERSION='0.9.0'

class Parser    
    def __init__(self):
        pass


class Lexer
    
#

def main():
    """
    Entry, argument parsing, and general sillines
    """    
    args = parse_args()

    pp.pprint( args )

    print yellow(args['url'])
    
    print blue(args['repo'])
    print darkred(args['repo_dir'])

    dest_exists = os.path.exists( args['repo_dir'] )
    full_path = os.path.abspath( args['repo_dir'] )
    
    print darkred( "Dest exists? %s" % dest_exists )

    if (args['clean'] and dest_exists) : 
        #Does your dog bite?
        #subprocess.call('rm -rf %s' % args['repo_dir'])
        print darkred( 'Removing: %s' %  args['repo_dir'] )
        shutil.rmtree( full_path )    

    if (not dest_exists):
        os.chdir( args['dest'] )
        subprocess.call(['git','clone', args['url'] ])
   
    parsed = clouseau( args['repo_dir'] )

    #To Do:
    #  Parsed is the intermediate representation.
    #  Better name the nodes
    #  Write a simple tree-walker with node events
    #    - on title node do something
    #    - on function node ...
    #    - on line_match node ...
    #    - etc.
    #
    # Silly dump
    #pp.pprint(parsed)
    #dump(parsed)
    





def parse_args():
    #print 'in parse args'
    p = arse.ArgumentParser (description="  Clouseau: A silly git inspector", version=VERSION)
    p.add_argument('--url', '-u', required=True, 
                    help="Fully qualified git URL (http://www.kernel.org/pub//software/scm/git/docs/git-clone.html)",
                    action="store", dest="url"
                  )
    p.add_argument('--patterns', '-p', required=False, help="Path to list of regular expressions to use.",
                    action="store", dest="patterns", type=file , default="patterns.txt")
    p.add_argument('--clean', '-c',  dest="clean", action="store_true", default=False, help="Delete the existing git repo and re-clone")
    p.add_argument('--output', '-o', dest="output_format", required=False, help="Output formats: markdown, raw, html, json")
    p.add_argument('--dest', '-d', dest="dest", default="temp", help="The directory where the git repo is stored. Default: ./temp")
    p.add_argument('--depth',type=int,required=False,help="The depth of the git-clone process. Default is all.")

    args = p.parse_args()
    url = args.url.rstrip('/')
    repo = url.rsplit('/',1)[1]
    repo_name = repo.rstrip('.git')
    return { "url": url,
             "repo": repo,
             "repo_name": repo_name,
             "repo_dir": ("%s/%s" % (args.dest,repo_name) ),
             "clean": args.clean,
             "output_format": args.output_format,
             "dest": args.dest

            }


def dump(clouseau_data):
    """
    Performs an app-specfic pretty print. This should look something like:
    # Title
    Tag line

    ## Term


    """
    pairs = [(k,v) for (k,v) in clouseau_data.items()]

    for key,value in pairs:
        print key
        #pp.pprint ( value.keys() )
        s = [ (kay,val) for (kay,val) in value.items() ]
        #t = [n for n in s.iteritems()]
        print( s )
        #if ( len(s) > 0 ):
        #s.sort()
        for  x,y in s:
            print teal(x)
            #print teal ( '%s == %s' % (x, y['matched_lines']) )
#        print ('%s has %d possible matches.' % (pair[0], s))

 

def clouseau(repo_dir):
    
    logging.basicConfig(level=logging.DEBUG)
    os.chdir( repo_dir )
    terms = ['cfpb', 'user', 'password']
    
    # Main results data structure
    clouseau = {}

    # - A collection of nodes
    ast_root = Node( type='root', value=None, parent=None )

    
    for term in terms:
        git_grep = subprocess.Popen(['git','grep','-inwap', '--heading', '--cached', '--no-color', '--break', term], stdout=subprocess.PIPE)
        # Maybe write it all to a file first, aka Raw.log, and then parse that, which could 
        # allow for multiple passes
        #stdout,stderr = git_grep.communicate()
        file_name_heading = re.compile( '^[a-zA-Z]' )
        function_name = re.compile( '^[0-9]+=' )
        matched_line = re.compile( '^[0-9]+:' ) 
        
        clouseau.update( {term: {}}  )

        
        for line in git_grep.stdout:
            if file_name_heading.match( line ):
                title = line.replace('/','_')
                title = title.replace('.','_')
                clouseau[term][title] = {'src' : line }
                node = Node( type='src', value='line', parent=ast_root )
                #print 'Key (parse): ' , title

            if function_name.match( line ):
                function = line.split('=')
                clouseau[term][title].update( {'function': function} ) 
                Node( type='function', value=function, parent=node )
                clouseau[term][title].update( {'matches': len(function)} ) 

            if matched_line.match( line ):
                clouseau[term][title].update( {'matched_lines': line.split(':',1)} )
                Node( type='matched_line', value=line.split(':',1), parent=node )

    pp.pprint ( ast_root )

    return clouseau 

#
# 
#
class Node:
    """
    Attempt to build an AST
    """

    def __init__(self, type,value,parent):
        self.type = type
        self.value = value
        self.parent = parent



if __name__ == '__main__':
    print bold( darkblue( '--------------- "Now do you or do you not have for me the massage?!!" ---------------') )
    main() 



