import pprint
import os
import xml
import sys


import xml.dom.minidom
from xml.dom.minidom import Node

class States:
	def __init__(self):
		#initialize values to empty or 0 values
		name = ""
		id = 0
		label = ""
		stateidle = ""
		
class Transitions:
	def __init__(self):
		#initialize values to empty or 0 values
		fr = 0
		read = ""
		to = 0
		response = ""
		keyword = ""	

class Test:
	def __init__(self):
		StateList = []
		TransitionList = []
		FILENAME = ""	
		infile = "testfull.jff"
		self.getXML(infile, StateList, TransitionList)
		try:	
			for St in StateList:
				print St.id
				print St.name
				print St.stateidle
				print St.label
			for Tran in TransitionList:
				print Tran.response
				print Tran.keyword
				print Tran.to
				print Tran.fr
				print Tran.read
		except AttributeError:
			print ""	
	def getXML(self, infile, StateList, TransitionList):
		#name of xml file in local
		(PATH, FILENAME) = os.path.split(infile)
		try:                          
			doc = xml.dom.minidom.parse(infile)
		except IOError:               # catch IOError and deriving exceptions
			print "Could not open\n"
			os._exit(99)
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
			  
		for node in doc.getElementsByTagName("transition"):
			fr = node.getElementsByTagName("from")
			read = node.getElementsByTagName("read")
			to = node.getElementsByTagName("to")
			response = node.getElementsByTagName("response")
			keyword = node.getElementsByTagName("keyword")
			y = Transitions()
			for node2 in fr:
				fr = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					fr += node3.data	  
					y.fr = fr
			for node2 in read:
				read = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					read += node3.data
					y.read = read
			for node2 in to:
				to	= ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					to += node3.data
					y.to = to
			for node2 in response:
				response = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					response += node3.data
					y.response = response
			for node2 in keyword:
				keyword	= ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					keyword += node3.data
					y.keyword = keyword
			TransitionList.append(y)
a = Test()