# Clouseau

A silly git repo inspector

### Status: Prenatal

- [ X ] Proof of concept
- [ ] Multiple output formats
- [ ] Works on reasonably sized repos
- [ ] Stores previous runs

The intent is that this can be run against any repo and it will search the index for 
file blobs containing the patterns defined in a ```patterns.txt``` file or a regular expression 
specified on the command line.


#### Current Usage

```$ bin/clouseau --url [repo-url]``` ; e.g., ```$ bin/clouseau --url https://github.com/virtix/cato.git``` 

Using a single regular expression:
```$ bin/couseau --url https://github.com/virtix/cato.git --term "Your Name"```


Searching the entire history (quite slow and needs work):
```$ bin/couseau --url https://github.com/virtix/cato.git --term "Your Name"  --pathspec all```


It should look something like this:

![](https://raw.github.com/virtix/clouseau/master/ss.png)


### Intended command-line interface 

```
$ bin/clouseau -h
usage: clouseau [-h] [-v] --url URL [--term TERM] [--patterns PATTERNS]
                [--clean] [--output OUTPUT_FORMAT]
                [--output-destination OUTPUT_DESTINATION] [--dest DEST]
                [--pathspec PATHSPEC]
                                                
Clouseau: A silly git inspector
                                                
 optional arguments:
   -h, --help               show this help message and exit
   -v, --version            show program's version number and exit
   --url URL, -u URL        Fully qualified git URL (http://www.kernel.org/pub//software/scm/git/docs/git-clone.html)
   --term TERM, -t TERM     Search for a single regular expression instead of every term in patterns.txt
   --patterns PATTERNS, -p PATTERNS
                            Path to list of regular expressions to use.
   --clean, -c              Delete the existing git repo and re-clone
   --output OUTPUT_FORMAT, -o OUTPUT_FORMAT
                            Output formats: console, markdown, raw, html, json
   --output-destination OUTPUT_DESTINATION, -od OUTPUT_DESTINATION
                            Location where the output is to be stored. Default ./temp.
   --dest DEST, -d DEST  The directory where the git repo is stored. Default: ./temp
   --pathspec PATHSPEC, -ps PATHSPEC
                            The pattern of files or commits to search. Default: HEAD. 
                            Specify 'all' to search the entire histtory.
   --before BEFORE, -b BEFORE
                            Search commits that occur prior to this date; e.g., Mar-08-2013
    --after AFTER, -a AFTER
                            Search commits that occur after this date; e.g., Mar-10-2013
    --author AUTHOR         Perform searched for commits made by AUTHOR; e.g., an email address or name.
