#!/bin/bash

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


echo "secure vars? $TRAVIS_SECURE_ENV_VARS"
echo "travis PR: $TRAVIS_PULL_REQUEST"
echo "bc: $BOTCLOUSEAU"
echo "$Revs: $REVS"
echo "Range: $TRAVIS_COMMIT_RANGE"

# Run clouseau
echo "Running Clouseau"
./bin/clouseau_thin -u https://github.com/$TRAVIS_REPO_SLUG --skip --dest $(dirname ../$(pwd)) --revlist="$REVS" > .clouseau_output.txt