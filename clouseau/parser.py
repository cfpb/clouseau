
import os
import sys
import re
import subprocess
import threading
from Queue import Queue

# -----------------------------------------------------------------------------------------------
class Parser:    
    """
    Converts git-grep's stdout to Python dictionary
    """
    
    def __init__( self ):
        pass

    def parse_terms( self, patterns_file, single_term ):
        terms = patterns_file.readlines()
        if( single_term != None ):
            terms = { single_term }
        terms = [term.strip() for term in terms if not term.startswith('#')]
        return terms
      


    def parse( self, terms, repo, **kwargs ):
        """
        For each term in @terms perform a search of the git repo and store search results
        (if any) in an iterable.
        """

        # Main results data structure
        clouseau = {}

        pathspec =  kwargs.get( 'pathspec' )
        before = kwargs.get( 'before' )
        after = kwargs.get( 'after' )
        author = kwargs.get( 'author' )
        github_url = kwargs.get( 'github_url' )
        git_dir = repo + '/.git'
        
        clouseau.update( {'meta' : {'github_url': github_url } } )

        revlist = self.generate_revlist( git_dir, pathspec, before, after, author )
              
        if (revlist == ''):
            #Need to build a more informative Nothing-found iterable
            return clouseau
        
        clouseau = self.search( git_dir, terms, revlist, clouseau )
        return clouseau
    
    
    #
    # Spawn a thread for each term
    #
    def search( self, git_dir, terms, revlist, clouseau ):
       
        queue = Queue()
        for t in terms:
            queue.put( t )
            search_thread = SearchThread( queue, git_dir, revlist, clouseau ) 
            search_thread.setDaemon( True )
            search_thread.start()

        return clouseau
    
    
    
    
    
    def generate_revlist(self, git_dir, pathspec, before, after, author):
            rev_list = None
            #Default rev list
            git_rev_cmd = ['git', '--git-dir', git_dir ,'rev-list', '--all', '--date-order']

            if ( author != None ):
                git_rev_cmd.append( '--author' )
                git_rev_cmd.append( author )
            if ( before != None ):
                git_rev_cmd.append( '--before' )
                git_rev_cmd.append( before )
    
            if ( after != None):
                git_rev_cmd.append( '--after' )
                git_rev_cmd.append( after )
    
            # ---
            if ( pathspec != None and pathspec.lower() == 'all' ):
                git_revlist = subprocess.Popen( git_rev_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
                rev_list = git_revlist.communicate()[0]
            elif (pathspec == None):
                git_revlist = subprocess.Popen( git_rev_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
                rev_list = git_revlist.communicate()[0]
            else:
                rev_list = pathspec


            return rev_list




# ----------------------------------------------------------------------------------------------
class SearchThread( threading.Thread ): 
    # Lexemes:
    file_name_heading = re.compile( '^[0-9a-zA-Z]{40}:.+$' )
    function_name = re.compile( '^[0-9]+=' )
    matched_line = re.compile( '^[0-9]+:' ) 


    def __init__ ( self, queue, git_dir, revlist, clouseau ):
        threading.Thread.__init__( self )
        self.queue = queue
        self.git_dir = git_dir
        self.revlist = revlist
        self.clouseau = clouseau



    def run( self ):
        while True:
            term = self.queue.get()
            self.run_search( term )
            self.queue.task_done()
        
        #self.queue.join()



    def run_search( self, term ):
        print "Running threaded search for term %s" % term

        git_grep_cmd = ['git','--git-dir', self.git_dir , 'grep','-inwa', '--heading', '--no-color', \
                                '--max-depth','-1', '-E', '--break', '--', term]
        
        cmd = git_grep_cmd + self.revlist.split()

        #print cmd

        # goes off into never-never land

        git_grep = subprocess.Popen( cmd , stderr=subprocess.PIPE, 
                                     stdout=subprocess.PIPE)

        (out,err) = git_grep.communicate()

        #print out


        self.clouseau.update( {term: {}}  )

        for line in out.split('\n'):
            # We don't  know how a lot of the data is encoded, so make sure it's utf-8 before 
            # processing
            if line == '':
                continue
            try:
                line = unicode( line, 'utf-8' ) 
            except UnicodeDecodeError:
                line = unicode( line, 'latin-1' ) 
            

            if self.file_name_heading.match( line ):
                title = line.split(':', 1)[1]
                title = line.replace('/','_')
                title = title.replace('.','_').strip()
                _src = line.strip().encode('utf-8')
                _srca = _src.split(':', 1)
                self.clouseau[term][title] = {'src' : _srca[1] }
                self.clouseau[term][title]['refspec'] =  _srca[0]
                git_log_cmd = subprocess.Popen( ['git', '--git-dir', self.git_dir , 'log', _srca[0] , '-1'],\
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE )
                git_log = git_log_cmd.communicate()[0]


                self.clouseau[term][title]['git_log'] = [ x.strip() for x in git_log.split('\n') if x != '' ]
                #clouseau[term][title] = {'ref' : _srca[0] }
                self.clouseau[term][title]['matched_lines'] = []
        

            if self.function_name.match( line ):
                function = line.split('=')
                self.clouseau[term][title].update( {'function': function} ) 
                self.clouseau[term][title].update( {'matches': len(function)} )

            if self.matched_line.match( line ):
                matched = line.split(':' , 1)
                matched[0] = matched[0].strip()
                matched[1] = matched[1].strip()
                self.clouseau[term][title]['matched_lines'].append( matched )
        
        return self.clouseau

