# Clouseau

A silly git repo inspector

### Status: Prenatal (not recommended for production use)

- [x] Proof of concept
- [ ] Multiple output formats
- [ ] Works on reasonably sized repos (concurrency)
- [ ] Stores previous runs

The intent is that this can be run against any repo and it will search the index for
file blobs containing the patterns defined in a ```patterns.txt``` file or a regular expression
specified on the command line.


#### Quick Setup

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


#### Current Usage

```$ bin/clouseau --url [repo-url]``` ; e.g., ```$ bin/clouseau --url https://github.com/virtix/cato.git```

Search the current revision using the default pattern file (clouseau/patterns/default.txt):
```$ clouseau -u https://github.com/virtix/cato.git```

Search using a single regular expression:
```$ bin/clouseau --url https://github.com/virtix/cato.git --term "Your Name"```

Search the entire history for a single term (quite slow and needs threading or multi-process work):
```$ bin/clouseau --url https://github.com/virtix/cato.git --term "Your Name"  --revlist all```

Search the current revision using a different pattern file:
```$ clouseau -u https://github.com/virtix/cato.git --patterns ~/projects/patterns/profanity.txt```

Search the current revision using multiple pattern files:
```$ clouseau -u https://github.com/virtix/cato.git --patterns ~/projects/patterns/profanity.txt,~/projects/patterns/custom_pattern.txt```

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

```

### Minimal Output

For continuous integration environments, minimal output may be desirable. In that case, use `bin/clouseau_thin`:

`$ bin/clouseau_thin -u [git_url] ...`

`clouseau_thin` supports all clouseau options and differs only in the verbosity and attractiveness of its output.

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

### Running with Docker

Clouseau is now in the Docker index and you can run it with a simple docker command:

```
docker run -i -e "GIT_URL=https://github.com/virtix/cato.git" -t dlapiduz/clouseau
```

## Getting involved

This section should detail why people should get involved and describe key areas you are
currently focusing on; e.g., trying to get feedback on features, fixing certain bugs, building
important pieces, etc.

General instructions on _how_ to contribute should be stated with a link to [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
