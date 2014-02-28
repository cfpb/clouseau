
import os
import sys
import re
import subprocess
import pprint
from clouseau_model import ClouseauModel


# -----------------------------------------------------------------------------------------------
class CommitParser:
    """
    Converts git-show's stdout to Python dictionary for any commit messages and file changes that match the terms in the patterns files
    """

    def __init__( self ):
        pass

    def parse( self, terms, repo, revlist, clouseau_model, **kwargs ):
        """
        For each term in @terms perform a search of the commits in the revlist and update the model with results
        """
        git_dir = repo + '/.git'

        for rev in revlist.strip().split(' '):
            output = self.get_commit(git_dir, rev)
            if output.strip() == '':
                print "WARNING: No output was returned from git for commit [%s]. Ensure the commit exists" % rev
            else:
                self.parse_commit( terms, output, clouseau_model )

    def get_commit(self, git_dir, commit):
        """
        Get the stdout of a call to `git show @commit --no-color --unified=0` for the directory specified by @git_dir
        """
        git_show_cmd = ['git', 'show', commit, '--no-color', '--unified=0']

        git_show = subprocess.Popen(git_show_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE) # , cwd=git_dir
        (out,err) = git_show.communicate()
        if err:
            print "ERROR running git command [%s]: %s" % (git_show_cmd, err)

        return out


    def parse_commit(self, terms, commit_output, clouseau_model):
        """
        @commit_output is the output of git-show
        @clouseau_model is the data structure we'll continue to update. Mutable State FTW
        """

        # First part will be the commit metadata... sha1, author, date, and body
        # Second part will be all the diffs. Each diff is demarcated with 'diff --git'

        # print commit_output

        parts = commit_output.split('diff --git', 1)

        git_log = [x.strip() for x in parts[0].split('\n') if x != ''] # consequently, the log body will always be git_log[3:]
        refspec = git_log[0].split(' ')[1] # grabs sha from 'commit d1859009afc7e48506ec025a07f4f90ce4c5a210'
        git_log_body = ' '.join(git_log[3:])

        ## Admittedly brittle... a commit message or a file in the commit that contains this string will hose the whole darn thing
        # So lame... TODO: Refactor
        if len(parts) == 1:
            diffs = parts[0].split('diff --git')
        else:
            diffs = parts[1].split('diff --git')

        for term in terms:
            term_re = re.compile(term, re.IGNORECASE)

            # inspect commit message
            if term_re.search(git_log_body):
                title = refspec + ":GIT_COMMIT_MESSAGE"
                title = clouseau_model.start_match(term=term, refspec=refspec, filename="Commit Message", git_log=git_log)
                clouseau_model.add_match_line(term, title, 1, git_log_body)
            # for each file, inspect lines
            for d in diffs:
                diff_lines = [x.strip() for x in d.split('\n') if x != '']
                (from_file, to_file) = self.diff_header_to_file_names(diff_lines[0])

                #TODO: Question: if a file is being deleted, should we even care?
                src = to_file if to_file != '' else from_file
                src_friendly = src.replace('.', '_')
                src_friendly = src_friendly.replace('/', '_')

                line_counter = 0
                for line in diff_lines:
                    title = refspec + ":" + src_friendly
                    #TODO: Should we care about deleted lines? Currently I'm only concerned with added/changed lines
                    if line.startswith('@@'):
                        line_counter = self.addition_start_line_from_chunk(line)

                    elif line.startswith('+'):
                        if term_re.search(line):
                            title = clouseau_model.start_match(term=term, refspec=refspec, filename=src, git_log=git_log)
                            clouseau_model.add_match_line(term=term, title=title, line_number=line_counter, match_text=line)
                        line_counter += 1


    # TODO: thoroughly unit test this. Must account for file additions and deletions
    def diff_header_to_file_names(self, header):
        """
        Takes input such as a/hooktest.txt b/hooktest.txt and returns the left and right filenames
        """
        left_right = header.strip().split(' ')
        left = left_right[0].lstrip('a/')
        right = left_right[1].lstrip('b/')
        return (left, right)

    # TODO: thoroughly unit test this. Must account for all types of additions/deletions/merges
    def addition_start_line_from_chunk(self, chunk):
        """
        Fetches the start line for additions from a chunk string such as @@ -5,0 +6,6 @@ Foo Bar
        """
        line_num_match = re.search('\+(\d+)', chunk)
        return int(line_num_match.group(0))
