#!/usr/bin/python
#coding=utf-8
import urllib2
import re
import os
import sys
import logging, traceback
import time
path = "/mnt/us/"

def parse(codes):
    ##logging.basicConfig(filename="getStory.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #rootLog = logging.getLogger()
    #rootLog.setLevel(logging.DEBUG)
    ########################################################
    #logging.info("Begin  ......\n")
    catalogFile = path  +"DK_News/"+ "Catalog_" + codes + ".txt"
    if os.path.exists(catalogFile)==True:
    	haveFile = open(catalogFile,"r")
    else:
    	haveFile = open(catalogFile,"w")
        haveFile.write("0")
    	haveFile.close()
    	haveFile = open(catalogFile,"r")
    
    currentNumber = int(haveFile.read())
    #print "currentNumber  ...... is " + str(currentNumber) + "\n"
    #logging.info("currentNumber  ...... is " + str(currentNumber) + "\n")
    haveFile.close()
    
    
    rootUrl = "http://www.biqugezw.com/" +codes + "/"
    rootResponse = urllib2.urlopen(rootUrl)
    m = re.findall('(<dd><a href="(.*)">(.*)</a></dd>)',rootResponse.read())
    for i in m:
    	number = int(re.compile("[/.]").split(i[1])[2])
    	#print "number  ...... is " + str(number) + "\n"
        if(number <= currentNumber):
            continue
        else:
            nextUrl = "http://www.biqugezw.com/" + i[1]
            if urlGet(nextUrl)==False:
                pass
            	#print nextUrl + "------>Error!!!"
            	#logging.info(nextUrl + "------>Error!!!\n")
    	    else: 
    	    	currentNumber = number
    	    	#print nextUrl + "------>Successfully!!!" 
            	#logging.info(nextUrl + "------>Successfully!!!\n")   
    
    
    haveFile = open(catalogFile,"w")
    haveFile.write(str(currentNumber))
    haveFile.close()
    print "Finished!!!"
    ##logging.info("Finished  currentNumber   is " + str(currentNumber) + "\n") 
##    sys.stdout.flush()
##    sys.stdout.flush()
    

def urlGet(url):
    try:
        response = urllib2.urlopen(url)
      
    except Exception:
        ##print url + "--------->  Error"
        logging.info(url + "--------->  Error\n") 
        return False
    ##print "Downloading " + url
    ##logging.info("Downloading " + url + "\n")
    downloadText(response.read())
    return True

def downloadText(text):
    m=re.findall("((<title>.+</title>)|((&nbsp;)+.+<br ))",text)
    title = m[0][0].replace("<title>","").replace("</title>","")
    ##output=open("/mnt/us/DK_Sync/" + title + ".txt",'w')
    ##print "Writing file " + title + ".txt"
    ##logging.info("Writing file " + title + ".txt\n")
    output=open(path + "DK_Sync/" + title + ".txt",'w')
    output.write(title);
    for i in m:
        output.write( i[0].replace("&nbsp;","").replace("<br",""))
    output.close()
