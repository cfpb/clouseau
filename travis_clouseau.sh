#!/bin/bash

function json_escape(){
  echo -n "$1" | python -c 'import json,sys; print json.dumps(sys.stdin.read())'
}

source ~/virtualenv/python2.7/bin/activate

# Get rev-list
if [ -n "$TRAVIS_COMMIT_RANGE" ]; then
    REVS=`git rev-list --abbrev-commit $TRAVIS_COMMIT_RANGE | tr '\n' ' '`
else
    REVS=$TRAVIS_COMMIT
fi

# Download clouseau
if [ ! -d "clouseau_run" ]; then
    wget -O clouseau_run.tar.gz http://github.com/marcesher/clouseau/archive/travis.tar.gz
    tar xfz clouseau_run.tar.gz
    mv clouseau-travis clouseau_run
fi

# Install clouseau
cd clouseau_run
export PYTHONPATH=$PYTHONPATH:.
pip install -r requirements.txt


echo "travis PR: $TRAVIS_PULL_REQUEST"
echo "Range: $TRAVIS_COMMIT_RANGE"
echo "Commit: $TRAVIS_COMMIT"


# Run clouseau
echo "Running Clouseau"
./bin/clouseau_thin -u https://github.com/$TRAVIS_REPO_SLUG --skip --dest $(dirname ../$(pwd)) --revlist="$REVS" > .clouseau_output.txt

output=$(<.clouseau_output.txt)
if [[ $output == *https://help.github.com/articles/remove-sensitive-data* ]]
then
  json_output=json_escape($output)
  curl -X POST -H "Content-Type: application/json" -d "'{\"body\":\"$json_output\"}'" https://api.github.com/repos/$TRAVIS_REPO_SLUG/commits/$TRAVIS_COMMIT/comments?access_token=$BOTCLOUSEAU
  exit 1
fi