#!/usr/bin/python
#coding=utf-8
import urllib2
import re
import os
import sys
path = "/mnt/us/DK_News/"

def parse(codes):
    catalogFile = path + "Catalog_" + codes + ".txt"
    if os.path.exists(catalogFile)==True:
    	haveFile = open(catalogFile,"r")
    else:
    	haveFile = open(catalogFile,"w")
        haveFile.write("0")
    	haveFile.close()
    	haveFile = open(catalogFile,"r")
    
    currentNumber = int(haveFile.read())
    haveFile.close()
    
    
    rootUrl = "http://www.biqugezw.com/" +codes + "/"
    rootResponse = urllib2.urlopen(rootUrl)
    m = re.findall('(<dd><a href="(.*)">(.*)</a></dd>)',rootResponse.read())
    for i in m:
    	number = int(re.compile("[/.]").split(i[1])[2])
        if(number < currentNumber):
            continue
        else:
            nextUrl = "http://www.biqugezw.com/" + i[1]
            if urlGet(nextUrl)==False:
            	print nextUrl + "------>Error!!!"
    	    else: 
    	    	currentNumber = number
    	    	print nextUrl + "------>Successfully!!!"    
    
    
    haveFile = open(catalogFile,"w")
    haveFile.write(str(currentNumber))
    haveFile.close()
    print "Finished!!!"
    sys.stdout.flush()
    sys.stdout.flush()
    

def urlGet(url):
    try:
        response = urllib2.urlopen(url)
      
    except Exception:
        print url + "--------->  Error"
        return False
    print "Downloading " + url
    downloadText(response.read())
    return True

def downloadText(text):
    m=re.findall("((<title>.+</title>)|((&nbsp;)+.+<br ))",text)
    title = m[0][0].replace("<title>","").replace("</title>","")
    ##output=open("/mnt/us/DK_Sync/" + title + ".txt",'w')
    print "Writing file " + title + ".txt"
    output=open(path + title + ".txt",'w')
    output.write(title);
    for i in m:
        output.write( i[0].replace("&nbsp;","").replace("<br",""))
    output.close()
