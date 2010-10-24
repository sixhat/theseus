#!/usr/bin/env python
# encoding: utf-8
"""
getUrl.py

Parses a downloaded RSS file and downloads all items in the Feed

Created by David Rodrigues on 2009-11-06.
Copyright (c) 2009 Sixhat Pirate Parts. All rights reserved.
"""

import sys
import os
import feedparser, time
import zlib

def main():
    # Parse the downloaded rss.xml file
    d=feedparser.parse(str(sys.argv[1])+"/rss.xml")
    
    urls=[] # The already downloaded list of URLS
    
    # Let's see if the downloaded list is present and construct the urls list
    try:
        f=open(sys.argv[1]+'/urls.txt','r+')
        for line in f:
            urls.append(line.split()[0])
    except Exception, e:
        f=open(sys.argv[1]+'/urls.txt','w')

    # Let's iterate over all entries in the parsed RSS
    for item in d.entries:  
        try:
            nome=str(item.updated_parsed[0])+"-"+str(item.updated_parsed[1])+"-"+str(item.updated_parsed[2])+"_"
            nome=nome+str(item.updated_parsed[3])+"h"+str(item.updated_parsed[4])+"m"+str(item.updated_parsed[6])+"s_"
        except:
            nome=time.strftime("%Y-%j_%H-%M-%S", time.gmtime())

        cifra=str(zlib.adler32(str(unicode(item.link).encode("utf-8"))))
        nome=nome+"_"+cifra+".html" # let's set the name of the output file based on the time

        if len(nome)>2:
            if len(item.link)>7:
                st="wget -t 3 -q --output-document=./"+sys.argv[1]+"/"+nome+" -U \"Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)\" \""+item.link+"\"" # This is the Bash command that we need to execute
                if unicode(item.link).encode("utf-8") not in urls:
                    #print item.link
                    os.system(unicode(st).encode("utf-8"))  #Execute the Download
                    f.write(unicode(item.link).encode("utf-8")+"\n") # Add this item to the downloaded URLS file
                    f.flush() # Let's flush the internal buffer
                    os.fsync(f.fileno()) # Let's force the write of all internal buffers to disk
                    time.sleep(int(sys.argv[2]));   # Wait TIMEOUT seconds to avoid DDoS blacklistings...
    f.close()

if __name__ == '__main__':
    if len(sys.argv)==3:
        main()

