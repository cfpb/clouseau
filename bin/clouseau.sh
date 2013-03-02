#!/bin/bash
#
#  Super simple proof-of-concept that pulls down the repo sepcified by $1 and then
#  looks in the repo for all the terms specified in patterns.txt. 
#
#  The "real one" is described in the enclosed Python modules
#
#  Usage:  ./clouseau.sh repo_name
#

echo $0 $1 $2



usage()
{
    echo
    echo "  Usage:  "
    echo "      clouseau.sh [repo-url] [repo-name]"
    echo
    echo "  Example:  "
    echo "      ./clouseau.sh  git://github.com/virtix/cato.git cata"
    echo
    exit -1
}


if [ -z $1 ]; then
    usage
fi     

if [ -z $2 ]; then
    usage
fi    


mkdir -p _temp
echo "Cloning $1"
rm -rf _temp/$2
cd _temp/
git clone $1
cd $2
pwd
IFS=$'\n'
   
for i in $(cat ../../patterns.txt); do
    git grep -iwap --heading --line-number --cached --break --color -- "$i"
done




# End.

