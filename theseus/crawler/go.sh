#!/usr/bin/env bash
set -xe

RSS=https://www.sixhat.net/rss.xml
TIMEOUT=10

THIS=$(dirname "$0")
DIR=$(date +%F)
TIM=$(date +%F-%H%M%S)
MYAGENT='Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'

# Let's be good citizens and ensure we are in the parent of the date dirs 
# where we'll archive stuff.
cd "$THIS"

# Try to create a Dir if we didn't that in a previous pass
mkdir -p "$DIR"

# if RSS exists and was successfully downloaded... 
# Call a python script to do the Parsing of the RSS file and to take care of 
# the download. Note that the Python Script calls 'wget' from inside its routine
# with an os.system call. Also note that after each successfull wget, we pause
# for 30 seconds before fetching another item of the RSS. This is to ensure 
# that the websites won't block us for DDoS atack. 
python getUrl.py "$DIR" "$TIMEOUT" "$RSS"

# Let's archive the RSS file...
mv "$DIR/rss.xml" "$DIR/rss_$TIM.xml"

# Closing stuff... and possible problems
#
# Naming Items by date isn't good. A digest should be implemented as some 
# malformed RSS feeds can set all the item.dates equal
# 


