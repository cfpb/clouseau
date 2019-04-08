# Clouseau


## What was Clouseau?

Clouseau was a command-line tool that we used to scan git repositories for personally identifiable information (PII), secret keys, and other credentials that we don't want to accidentally commit. 

We've decided that a more promising way to solve this problem is by utilizing the git-secrets project: https://github.com/awslabs/git-secrets

This repo continues to exist to store the Clouseau library of patterns, somewhat reformatted for git-secrets compatibility.

## Dependencies

 - [git-secrets](https://github.com/awslabs/git-secrets), and anything it depends on.


## Quick setup

1. Install git-secrets (homebrew users may wish to `brew install git-secrets --HEAD`)

1. Check this repo out to your filesystem

1. Install the Clouseau default patterns into git-secrets with `git secrets  --add-provider -- grep -v \#  /path/to/clouseau/patterns/default.txt`

1. Install the Clouseau profanity patterns into git-secrets with `git secrets  --add-provider -- grep -v \#  /path/to/clouseau/patterns/profanity.txt`

Once you've followed those steps, you'll be able to use [`git secrets --scan`](https://github.com/awslabs/git-secrets#options-for-scan) and [`git secrets --scan-history`](https://github.com/awslabs/git-secrets#operation-modes) to search a given repository for secrets.

You can set up commit hooks in a particular repo with:

```
git secrets --install
```

Or install the secrets hooks globally (for **newly created or cloned repos only**):

```
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets
```

For existing repos, you will want to go back and `git secrets --install` as described above.



## Usage

See [the git-secrets README](https://github.com/awslabs/git-secrets#synopsis) for details of scanning your repo (and its history), and installing commit hooks to scan for secrets automatically.


## Getting involved

If you're interested in using the Clouseau library of patterns to scan your source code and commit messages for undesirable content,
please get involved. We especially appreciate new and updated patterns that will help keep repos free of risky data!

General instructions on _how_ to contribute are described in [CONTRIBUTING](CONTRIBUTING.md).


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
