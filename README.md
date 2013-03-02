# Clouseau

A silly git repo inspector


The intent is that this can be run against any repo and it will search the index and tree for 
file blobs containing the patterns defined in ```patterns.txt```.  The shell script is a quick
 and dirty proof-of-concept; that is, it needs to be run manually and requires a human to inspect 
 the output.


There is the start of a newer Python app that parses the git-grep output to a some TBD data structure.



#### Current Usage

```$ ./clouseau.sh [repo-url] [repo-name]``` 

Example:  

```$ ./clouseau.sh git://github.com/virtix/cato.git cato```







