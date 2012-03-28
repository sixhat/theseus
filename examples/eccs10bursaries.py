#!/usr/bin/env python
# encoding: utf-8
"""
eccs10bursaries.py
==================

This example will demonstrate the use of Theseus to process a set of texts
that are archived in a folder ./TXT

Text Files are named 01.txt ... 11.txt
"""

import sys
import os
import theseus.processor.theseus as theseus
from operator import itemgetter

def main():
    """
    This example will demonstrate the use of Theseus to process a set of texts
    that are archived in a folder ./TXT

    Text Files are named 01.txt ... 11.txt
    
    Check the source code to detailed step by step instructions
    """
    # 1. Let's get a List of TXT Files in the Directory
    
    path="./TXT/"
    dirList=os.listdir(path)
    
    # 2. Let's create a Channel and a Domain
    
    reports = theseus.Channel('ECCS10 Bursaries')
    dom = theseus.Domain('ECCS10 Bursaries')
    
    # 3. Let's load each Text File into a DocNode and add this DocNode to the Channel
    docs=[]
    for file in dirList:
        # 3.0 - Check to see if file has a .txt extension
        if file[-4:]!=".txt":
            continue
        
        # 3.1 - Read File
        f=open(path+file,'r')
        # 3.1.1 Pay attention to encoding problems with text. In this case we convert everything to utf8
        txt=unicode(f.read(), 'utf8')
        f.close()
        
        # 2 - Create new DocNode
        doc=theseus.DocNode()
        # 3.2.1 - set txt of DocNode and name
        doc.txt=txt
        doc.fnm=file
        # 3.2.2 - extract sentences of DocNode - this cleans the text on each sentence
        doc.extractSentences()
                
        # 3.3 Lets add these words to our Domain
        for sentence in doc.sentences:
            dom.addWords(sentence.cleanedWords)
        
        # 3.4 Let's add this document to the reports channel
        reports.addDocument(doc)
        docs.append(doc)

    # 4. Let's export the Domain to a File
    dom.exportDomain()
    
    # 5. Let's iterate over the reports Channel's Documents to calculate the score of each sentence
    phrases={}

    for document in reports.documents:
        print "="*40, "Processing ", document.fnm, "="*40
        for sentence in document.sentences:
            print sentence.text
            # 5.1 Calculate the score of each sentence (_sscore) and also the word score (_wscore)
            sentence._sscore=0.0
            sentence._wscore=[]
            for word in sentence.cleanedWords:
                value=theseus.tfpdf(word,[reports])
                sentence._sscore+=value
                sentence._wscore.append(value)
            # 5.2 Store the phrase and score
            phrases[sentence]=sentence._sscore

    # 6. Generate a sorted list of Sentences
    print "="*100
    newd=sorted(phrases.items(), key=itemgetter(1), reverse=True)
    
    for ph,sc in newd:
        print sc,"\t"+ph.text
    

if __name__ == '__main__':
    main()
