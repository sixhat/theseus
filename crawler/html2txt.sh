#!/bin/bash
# 2010 - David Rodrigues
# Converts a journals entries into text files in a "txt" folder inside each day
#
jornal=$1
hoje=`date +%F`


function help {
        echo
        echo "Usage: ./html2txt <Journal Dir>"
        echo
        exit
}

if [ -z $jornal ]
    then
        help
fi

if [ -d "$jornal" ]
    then
        echo Changing into $jornal Directory
    else
        help
fi

cd $jornal

for dd in 20*
do
# We don't process todays directory
	if [ $dd != $hoje ]
		then 
		echo Entering $dd
        cd $dd
        mkdir -p "txt"
        for f in *.html
        do
            lynx -dump $f > txt/$f.txt
        done
        cd ..
	fi
done


