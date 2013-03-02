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

#pp = pprint.PrettyPrinter()

VERSION='0.9.0'


class Clouseau:
    """
    Wrap and delegate
    """
    

    def __init__(self):
        pass

    def parse_args( self, arguments ):

        print ( os.path.abspath( 'clouseau/patterns/patterns.txt' ) )
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

    def parse(program):
        parsed ='123'
        return parsed


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
