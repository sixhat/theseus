#!/bin/bash
# 2010 - David Rodrigues
# Converts a journal into a Zip File and deletes the zipped folders (carefull)
# 

jornal=$1
hoje=`date +%F`

function help {
        echo
        echo "Usage: ./j2zip <Journal Dir>"
        echo 
        exit
}

if [ -z $jornal ] 
    then 
        help 
fi

if [ -d "$jornal" ] 
    then
        echo All Good
    else 
        help
fi

echo Changing into $jornal Directory
cd $jornal

for dd in 20*
do
# We don't process todays directory
	if [ $dd != $hoje ]
		then 
            zip -m -r -9 $jornal-$hoje.zip $dd
	fi
done


