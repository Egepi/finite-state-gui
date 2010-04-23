import pprint
import os
import xml
import sys
import re
import glob

import xml.dom.minidom
from xml.dom.minidom import Node
	
class States:
	def __init__(self):
		#initialize values to empty or 0 values
		name = ""
		id = 0
		label = ""
		stateidle = ""
		


	#name of xml file in local
	StateList = []
	FILENAME = ""	
	infile = "template.jff"
(PATH, FILENAME) = os.path.split(infile)
try:                          
	doc = xml.dom.minidom.parse(infile)
except IOError:               # catch IOError and deriving exceptions
	print "Could not open\n"
	os._exit(99)
else:                         # optional, run block if no exception thrown
	print "Parsing:",FILENAME, "\n"
	  
for node in doc.getElementsByTagName("state"):
	id = node.getAttribute("id")
	name = node.getAttribute("name")
	stateidle = node.getElementsByTagName("stateIdleResp")
	label = node.getElementsByTagName("label")
	x = States()
	x.id = id
	x.name = name
	for node2 in stateidle:
		stateidle = ""
	for node3 in node2.childNodes:
		if node3.nodeType == Node.TEXT_NODE:
			stateidle += node3.data	
			x.stateidle = stateidle
			#save to state object put into lists
	for node2 in label:
		label = ""
	for node3 in node2.childNodes:
		if node3.nodeType == Node.TEXT_NODE:
			label += node3.data	
			x.label = label
	StateList.append(x)
		  
		
for States in StateList:
	print States.id