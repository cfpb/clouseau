# Clouseau

[![Build Status](https://travis-ci.org/cfpb/clouseau.svg)](https://travis-ci.org/cfpb/clouseau)


## What is Clouseau?

Clouseau is a silly git repo inspector. 

Clouseau is a P.I. for your PII. It searches git commits -- source code and commit messages -- for undesirable text patterns, such as passwords, ssh keys and personal identifiable information. You can search for profanity or other information with a new pattern file or a regular expression specified on the command line. 

See the **Get Involved** section at the end of this readme to see the current status of this project and contribute.

## Dependencies

 - Unix-based OS, such as Mac or Linux (Windows support is unclear at this time.) 
 - [git](http://git-scm.com/)
 - [Python 2.7](https://www.python.org/download/releases/2.7/)
 - [virtualenv](https://virtualenv.pypa.io/en/latest/)
 
See the [requirements.txt](requirements.txt) file for additional dependencies to be installed in the quick setup.


## Quick setup

1. Clone this repository somewhere you can execute Python code.

1. From the cloned Clouseau project root, set up a virtualenv:
   ```sh
   virtualenv --no-site-packages --distribute venv    # creates the virtualenv named "venv"
   source venv/bin/activate                           # activates (places you in) the virtualenv
   ```

1. Install the requirements:
   ```sh
   pip install -r requirements.txt
   ```

4. Tell Python to also look in this directory for libraries.
   ```sh
   export PYTHONPATH=$PYTHONPATH:.
   ```

And that's it! Now follow the usage instructions below.


## Basic Usage

Search a github repository to match patterns:

```$ bin/clouseau --url [repo-url]``` ; e.g., ```$ bin/clouseau --url https://github.com/virtix/cato.git```

This will search against the default pattern file (`clouseau/patterns/default.txt`) and display any matches for each of the patterns the file contains.  
  
  
The results should look something like this:

![](https://raw.github.com/cfpb/clouseau/master/ss.png)


## Additional Usage Options

Search using a single regular expression:  
```$ bin/clouseau --url https://github.com/virtix/cato.git --term "Your Name"```

Search the entire history for a single term (quite slow and needs threading or multi-process work):  
```$ bin/clouseau --url https://github.com/virtix/cato.git --term "Your Name"  --revlist all```

Search the current revision using a different pattern file:  
```$ bin/clouseau -u https://github.com/virtix/cato.git --patterns ~/projects/patterns/profanity.txt```

Search the current revision using multiple pattern files:  
```$ bin/clouseau -u https://github.com/virtix/cato.git --patterns ~/projects/patterns/profanity.txt,~/projects/patterns/custom_pattern.txt```

Skip either cloning or pulling and just scan:  
```$ bin/clouseau -u https://github.com/virtix/cato.git --skip```

Search the specific revision :  
```$ bin/clouseau -u https://github.com/virtix/cato.git --revlist 5c0b30b007```

Search between the range of two commits:  
```$ bin/clouseau -u https://gituhub.com/virtix/cato.git --revlist d46868fe...3ea013e8```

Search since a given date:  
```$  bin/clouseau -u https://github.com/virtix/cato.git --after 03/10/13```

Blame:  
```$ bin/clouseau -u https://github.com/virtix/cato.git --author bill```


### Intended command-line interface

```
$ bin/clouseau -h
usage: clouseau [-h] [-v] --url URL [--term TERM] [--patterns PATTERNS]
                [--clean] [--output OUTPUT_FORMAT]
                [--output-destination OUTPUT_DESTINATION] [--dest DEST]
                [--revlist REVLIST]

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

```

### Minimal output

For continuous integration environments, minimal output may be desirable. In that case, use `bin/clouseau_thin`:

`$ bin/clouseau_thin -u [git_url] ...`

`clouseau_thin` supports all clouseau options and differs only in the verbosity and attractiveness of its output.

### Running locally on a cloned repository

Run Clouseau from your cloned project root, with your repository's Github url in place of $remote_url:

`$ clouseau_thin -u $remote_url --skip --dest $(dirname $(pwd)) --revlist="HEAD"`

This is useful for checking local repositories for sensitive data before pushing to a public URL.

### Running as a `post-commit` hook

First, install Clouseau by changing directory to your cloned Clouseau project root and then `pip install -e ./`

Test the install by changing to any other directory and issuing `clouseau` and also `clouseau_thin`

Now, change to one of your local git repos.

Create `.git/hooks/post-commit` and make it executable (`chmod +x .git/hooks/post-commit`)

Edit it with content such as this:

```
#!/bin/sh

echo "running clouseau"
remote_url=$(git config --get remote.origin.url)
clouseau_thin -u $remote_url --skip --dest $(dirname $(pwd)) --revlist="HEAD"
```

Now, make a commit to that project.

You should see that Clouseau runs and finds nothing.

Make another commit, this time adding something that looks like a SSN or IP to the file and/or the commit message.
Run Clouseau again, and you should see output such as this:

```
running clouseau
Skipping git-clone or git-pull as --skip was found on the command line.
Clouseau: a silly git inspector, searching [your_git_url]

✓  hooktest.txt
Search term:  username[ ]*=[ ]*.+
git@github.com:marcesher/cato/commit/0731c34b40bcd4322c6b4daf044ec3587211808a
Author: Marc Esher <marc.esher@gmail.com> Date:   Tue Feb 25 15:41:37 2014 -0500
my username=foo

+production_ip=127.0.0.1  Line:19
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

✓  Commit Message
Search term:  username[ ]*=[ ]*.+
git@github.com:marcesher/cato/commit/0731c34b40bcd4322c6b4daf044ec3587211808a
Author: Marc Esher <marc.esher@gmail.com> Date:   Tue Feb 25 15:41:37 2014 -0500
my username=foo

my username=foo  Line:1
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
```

Clouseau's output can also [be sent to the Mac OS X Notification Center via post-commit hook](https://github.com/willbarton/clouseau-notification-hook/blob/master/post-commit.notification), which is useful for users of GitHub's GUI client for Mac.

### Running with Docker

Clouseau is now in the Docker index and you can run it with a simple docker command:

```
docker run -i -e "GIT_URL=https://github.com/virtix/cato.git" -t dlapiduz/clouseau
```

## Running unit tests

To run unit tests, issue:

```sh
nosetests
```


## Getting involved

If you're interested in using Clouseau to scan your source code and commit messages for undesirable content,
please get involved.

Clouseau is currently in an early stage of development and not recommended for production use.

- [x] Proof of concept
- [ ] Multiple output formats
- [ ] Works on reasonably sized repos (concurrency)
- [ ] Stores previous runs

The intent is that this can be run against any repo and it will search the index for
file blobs containing the patterns defined in a ```patterns.txt``` file or a regular expression
specified on the command line.

We welcome feature requests, bug reports, and code / documentation improvements.
We also welcome stories of how you're using Clouseau.

General instructions on _how_ to contribute are described in [CONTRIBUTING](CONTRIBUTING.md).


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
