#!/usr/bin/env bash
set -xe
# 
# v0.1
# Created by David Rodrigues on 2009-11-06.
# Copyright (c) 2009 Sixhat Pirate Parts. All rights reserved.

RSS=https://www.sixhat.net/rss.xml
TIMEOUT=140

THIS=`dirname "$0"`
DIR=`date +%F`
TIM=`date +%F-%H%M%S`
MYAGENT='Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'

# Let's be good citizens and ensure we are in the parent of the date dirs 
# where we'll archive stuff.
cd $THIS

# Try to create a Dir if we didn't that in a previous pass
mkdir -p $DIR

# Download The Latest RSS File From The Newspaper
wget -t 3 -q -U "$MYAGENT" $RSS -O $DIR/rss.xml

# if RSS exists and was successfully downloaded... 
if [ -f "$DIR/rss.xml" ]
then 
# Call a python script to do the Parsing of the RSS file and to take care of 
# the download. Note that the Python Script calls 'wget' from inside its routine
# with an os.system call. Also note that after each successfull wget, we pause
# for 30 seconds before fetching another item of the RSS. This is to ensure 
# that the websites won't block us for DDoS atack. 
python getUrl.py $DIR $TIMEOUT

# Let's archive the RSS file...
mv $DIR/rss.xml $DIR/rss_$TIM.xml
fi

# Closing stuff... and possible problems
#
# Naming Items by date isn't good. A digest should be implemented as some 
# malformed RSS feeds can set all the item.dates equal
# 


