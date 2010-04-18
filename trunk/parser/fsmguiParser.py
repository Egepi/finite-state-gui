# FSMGUI XML ('jff') to Python Parser
# Author: Jennifer Kinahan

import pprint
import os
import xml
import sys
import re
import glob
 
import xml.dom.minidom
from xml.dom.minidom import Node

#Path of the folder where all the files are stored.
#Note: CHANGE THIS TO INCORPORATE THE XML FILES YOU WANT TO BE PARSED
path = 'C:\Users\YT\Documents\EVL\ProjectLifelike\FSMGUI\parser'
# parse through all .xml documents within given path
for infile in glob.glob(os.path.join(path, '*.jff')):
    
    # infile stores the complete path of the file
    print "Current File Being Processed is:  " + infile 
    #use split, display both path and filename of files being parsed
    (PATH, FILENAME) = os.path.split(infile)
    print " PATH is " + PATH
    print " FILENAME is " + FILENAME
	
try:                          
  doc = xml.dom.minidom.parse(infile)
except IOError:               # catch IOError and deriving exceptions
  print "Could not open\n"
  os._exit(99)
else:                         # optional, run block if no exception thrown
  print "Parsing:",FILENAME, "\n"
  
mapping = {}
  
for node in doc.getElementsByTagName("state"):
  id = node.getAttribute("id")
  name = node.getAttribute("name")
  stateidle = node.getElementsByTagName("stateIdleResp")
  label = node.getElementsByTagName("label")
  for node2 in stateidle:
	stateidle = ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		stateidle += node3.data	
  for node2 in label:
	label = ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		label += node3.data	
		
  mapping[stateidle] = "stateidle: " + stateidle
  mapping[label] = "label: " + label

for node in doc.getElementsByTagName("transition"):
  fr = node.getElementsByTagName("from")
  read = node.getElementsByTagName("read")
  to = node.getElementsByTagName("to")
  response = node.getElementsByTagName("response")
  keyword = node.getElementsByTagName("keyword")
  for node2 in fr:
	fr = ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		fr += node3.data	  
  for node2 in read:
	read = ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		read += node3.data	  
  for node2 in to:
	to	= ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		to += node3.data
  for node2 in response:
	response = ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		response += node3.data	  
  for node2 in keyword:
	keyword	= ""
  for node3 in node2.childNodes:
	if node3.nodeType == Node.TEXT_NODE:
		keyword += node3.data	

  mapping[fr] = "fr: " + fr 
  mapping[to] = "to: " + to
  mapping[response] = "resp: " + response
  mapping[keyword] = "key: " + keyword
  mapping[read] = "read: " + read		
pprint.pprint(mapping)