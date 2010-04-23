import pprint
import os
import xml
import sys
import re
import glob

import xml.dom.minidom
from xml.dom.minidom import Node

# INI state function
def FSM_INI_Func(activity, str):
	activity.speak('what do you want to know? I can tell you weather or news.')

# Testing state function
def FSM_TEST_Func(activity, str):
	activity.speak('hi i am testin this.')

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


class WTH():
	#initialize
	def __init__(self):
		StateList = []
		TransitionList = []
		FILENAME = ""
		infile = "template.jff"	
		count = 0
		#name of xml file in local
		(PATH, FILENAME) = os.path.split(infile)
		
		self.getXML(infile, FILENAME, StateList, TransitionList, States, Transitions)
		self.RootInitGenerator(FILENAME, StateList, TransitionList)
		self.stateGenerator(FILENAME, StateList, TransitionList)		
		for Statesa in StateList:
			print Statesa.name
			print "A"
	#Create and add a state and all of its transitions
	def stateGenerator (self, FILENAME, StateList, TransitionList):
\
		for States in StateList:
			#States = StateList.pop(0); 
			count = 0
			tempName = FILENAME + "_" + States.name
			#gramid = self.addGrammar(tempName + "_GRM")
			#self.currentGrammarID = gramid
			#self.grammarIDs[tempName] = gramid
			print States.name
			print "Z"
			for Transitions in TransitionList:
				if States.id == Transitions.fr:
					#ruleid = self.addGrammarRule(gramid, tempName + "_R"+count, Transitions.keyword)
					#self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
					TransitionList.remove(Transitions)
					count = count+1
			StateList.remove(States) #at this i
			#if not States:
			#	print "end of StatesList"
			#	os._exit(99)
	
	#create root/init states then call state generator
	def RootInitGenerator(self, FILENAME, StateList, TransitionList):		
		# Map (input, current_state) --> (action, next_state)
		# action is state related function assigned to it
		#self.state_transitions = {}
		#self.grammarIDs = {}
		#self.exiting = False
		#self.active = False
			
		# initial state
		#self.initial_state = FILENAME + '_INI'
		#self.current_state = self.initial_state
		#self.action = FSM_INI_Func
		#self.initial_action = FSM_INI_Func
		#self.next_state = None
		#self.prev_state = None
			
		# register transition to this activity from ActivityManager (top level manager)
		# use ':' as delim for multiple recognizable inputs
		#self.registerTransition("test:testing")
		
		#ROOT STATE 
		count = 0;
		States = StateList.pop(0);
		tempName = FILENAME + "_ROOT"
		#gramid = self.addGrammar(tempName+"_GRM")
		#self.grammarIDs[tempName] = gramid
		for Transitions in TransitionList:
			if States.id == Transitions.fr:
				#ruleid = self.addGrammarRule(gramid, tempName+"_R"+count, Transitions.keyword)
				#self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
				TransitionList.remove(Transitions);
				count = count + 1
		
		#INI STATE
		count = 0;
		States = StateList.pop(0);
		tempName = FILENAME + "_INI"
		#gramid = self.addGrammar(tempName + "_GRM")
		#self.grammarIDs[tempName] = gramid

		for Transitions in TransitionList:
			if States.id == Transitions.fr:
				#ruleid = self.addGrammarRule(gramid, tempName + "_R" + count, Transitions.keyword)
				#self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
				TransitionList.remove(Transitions);
				count = count+1 
			
	#XML parsing
	def getXML(self, infile, FILENAME, StateList, TransitionList, States, Transitions):

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
			
A  = WTH()