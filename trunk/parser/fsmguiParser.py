# FSMGUI XML to Python Parser
# Author: Jennifer Kinahan

import pprint
import os
 
import xml.dom.minidom
from xml.dom.minidom import Node

s = "Please type which file you would like to parse within your FSMGUI folder: \nExample: 'books.xml'\n\n"
filename = raw_input(s)

print "Searching for:",filename, "\n"

try:                          # wrap "dangerous" code in a try block
  doc = xml.dom.minidom.parse(filename)
except IOError:               # catch IOError and deriving exceptions
  print "Could not open\n"
  os._exit(99)
else:                         # optional, run block if no exception thrown
  print "Parsing:",filename, "\n"
  
mapping = {}
  
for node in doc.getElementsByTagName("state"):
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