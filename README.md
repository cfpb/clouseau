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





