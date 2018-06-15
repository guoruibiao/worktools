#!/usr/bin bash
# myman command

DOCS_PATH="/home/tools/myman/docs"
AVAIABLE_COMMANDS=`ls $DOCS_PATH | tr "\t" "\n"`
echo ""
for item in ${AVAIABLE_COMMANDS[@]}
do
    if test  "$1" == "$item";then
        cat $DOCS_PATH/$1
        exit 0
    fi
done
echo "Command ["$1"] not found." 
