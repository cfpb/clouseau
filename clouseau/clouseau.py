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
import sys
from colors import *

#pp = pprint.PrettyPrinter()

VERSION='0.9.0'


class Clouseau:
    """
    Wrap and delegate
    """
    

    def __init__(self):
        pass

    def clone_repo(self, url, destination):
        try:
            _out = subprocess.check_output(['git', 'clone', url, destination])        
        
        except subprocess.CalledProcessError:
            print blue( "Directory, %s, exits. Trying git-pull instead of clone." % destination )
            _out = subprocess.check_output(['git', '--git-dir=%s/.git' % destination, 'pull'])       
            print smoke( "Git says: %s" % _out )
        
        except :
            e = sys.exc_info()[0]
            print red( 'Problem writing to destination: %s' % destination ) 
            raise
        
        return _out
            


    def parse_args( self, arguments ):

        #print ( os.path.abspath( 'clouseau/patterns/patterns.txt' ) )
        p = arse.ArgumentParser (description="  Clouseau: A silly git inspector", version=VERSION)
        p.add_argument('--url', '-u', required=True, 
                        help="Fully qualified git URL (http://www.kernel.org/pub//software/scm/git/docs/git-clone.html)",
                        action="store", dest="url"
                      )
        p.add_argument('--patterns', '-p', help="Path to list of regular expressions to use.",
                         action="store", dest="patterns", type=file , default="clouseau/patterns/patterns.txt")
        p.add_argument('--clean', '-c',  dest="clean", action="store_true", default=False, help="Delete the existing git repo and re-clone")
        p.add_argument('--output', '-o', dest="output_format", required=False, help="Output formats: markdown, raw, html, json")
        p.add_argument('--dest', '-d', dest="dest", default="temp", help="The directory where the git repo is stored. Default: ./temp")
        p.add_argument('--depth',type=int,required=False,help="The depth of the git-clone process. Default is all.")

        args = p.parse_args( arguments )
        url = args.url.rstrip('/')
        repo = url.rsplit('/',1)[1]
        repo_name = repo.rstrip('.git')
        self.args = args
        return { "url": url,
                 "repo": repo,
                 "repo_name": repo_name,
                 "repo_dir": ("%s/%s" % (args.dest,repo_name) ),
                 "clean": args.clean,
                 "output_format": args.output_format,
                 "dest": args.dest,
                 "patterns": args.patterns
              }






class Parser:    
    
    def __init__(self):
        pass

    def parse(self, terms, repo):
        
        # Lexemes:
        file_name_heading = re.compile( '^[a-zA-Z]' )
        function_name = re.compile( '^[0-9]+=' )            
        matched_line = re.compile( '^[0-9]+:' ) 
        
        # Main results data structure
        clouseau = {}

        # - A collection of nodes
        ast_root = Node( type='root', value=None, parent=None )
        os.chdir( repo )
        
        for term in terms:
            git_grep = subprocess.Popen(['git','grep','-inwa', '--heading', '--cached', '--no-color', '--break', term], stdout=subprocess.PIPE)
            # Maybe write it all to a file first, aka Raw.log, and then parse that, which could 
            # allow for multiple passes
        
            clouseau.update( {term: {}}  )
        
            for line in git_grep.stdout:
               # print blue( "Line: " ), line

                if file_name_heading.match( line ):
                    title = line.replace('/','_')
                    title = title.replace('.','_').strip()
                    clouseau[term][title] = {'src' : line.strip() }
                    clouseau[term][title]['matched_lines'] = []
                    #node = Node( type='src', value='line', parent=ast_root )
                    #print 'Key (parse): ' , title

                if function_name.match( line ):
                    function = line.split('=')
                    clouseau[term][title].update( {'function': function} ) 
                    #Node( type='function', value=function, parent=node )
                    clouseau[term][title].update( {'matches': len(function)} ) 

                if matched_line.match( line ):
                    matched = line.split(':' , 1)
                    matched[0] = matched[0].strip()
                    matched[1] = matched[1].strip()
                    clouseau[term][title]['matched_lines'].append( matched )
                    #Node( type='matched_line', value=line.split(':',1), parent=node )

        return clouseau


class Node:

    def __init__(self,type,value,parent):
        self.type = type
        self.value = value
        self.parent = parent

    def visit(self, _lambda):
        """
        Recursivley visits this node and all children 
        """
        pass
