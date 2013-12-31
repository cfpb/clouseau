# Clouseau

A silly git repo inspector

### Status: Prenatal (not recommended for production use)

- [ X ] Proof of concept
- [ ] Multiple output formats
- [ ] Works on reasonably sized repos (concurrency)
- [ ] Stores previous runs

The intent is that this can be run against any repo and it will search the index for 
file blobs containing the patterns defined in a ```patterns.txt``` file or a regular expression 
specified on the command line.


#### Quick Setup

1. Clone this repository somewhere you can execute Python code.

2. From the project root, set up a virtualenv:

```sh
virtualenv --no-site-packages --distribute venv    # creates the virtualenv named "venv"
source venv/bin/activate                           # activates (places you in) the virtualenv
```

3. Install the requirements:

```sh
pip install -r requirements.txt
```

4. Tell Python to also look in this directory for libraries.

```sh
export PYTHONPATH=$PYTHONPATH:.
```

And that's it! Now follow the usage instructions below.


#### Current Usage

```$ bin/clouseau --url [repo-url]``` ; e.g., ```$ bin/clouseau --url https://github.com/virtix/cato.git``` 

Search the current revision using the default pattern file (clouseau/patterns/default.txt):
```$ clouseau -u https://github.com/virtix/cato.git```

Search using a single regular expression:
```$ bin/couseau --url https://github.com/virtix/cato.git --term "Your Name"```

Search the entire history for a single term (quite slow and needs threading or multi-process work):
```$ bin/couseau --url https://github.com/virtix/cato.git --term "Your Name"  --revlist all```

Search the current revision using a different pattern file:
```$ clouseau -u https://github.com/virtix/cato.git --patterns ~/projects/patterns/profanity.txt```

Skip either cloning or pulling and just scan:
```$ clouseau -u https://github.com/virtix/cato.git --skip```

Search the specific revision :
```$ clouseau -u https://github.com/virtix/cato.git --revlist 5c0b30b007```

Search between the range onf two commits:
```$ clouseau -u https://gituhub.com/virtix/cato.git --revlist d46868fe...3ea013e8```

Search since a given date:
```$  clouseau -u https://github.com/virtix/cato.git --after 03/10/13```

Blame:
```$ clouseau -u https://github.com/virtix/cato.git --author bill```


            

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
   --output OUTPUT_FORMAT, -o OUTPUT_FORMAT  (NOT YET IMPLEMENTED)
                            Output formats: console, markdown, raw, html, json
   --output-destination OUTPUT_DESTINATION, -od OUTPUT_DESTINATION  (NOT YET IMPLEMENTED)
                            Location where the output is to be stored. Default ./temp.
   --dest DEST, -d DEST  The directory where the git repo is stored. Default: ./temp  (NOT YET IMPLEMENTED)
   --revlist REVLIST, -rl REVLIST
                           A space-delimted list of revisions (commits) to search. 
                           Defaults to HEAD. Specify 'all' to search the entire history.
   --before BEFORE, -b BEFORE
                            Search commits that occur prior to this date; e.g., Mar-08-2013
    --after AFTER, -a AFTER
                            Search commits that occur after this date; e.g., Mar-10-2013
    --author AUTHOR         Perform searched for commits made by AUTHOR; e.g., an email address or name.
    --skip   SKIP           If specified, skips any calls to git-clone or git-pull.
