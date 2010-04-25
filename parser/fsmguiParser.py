# FSMGUI XML ('jff') to Python Parser
# Authors: Jennifer Kinahan & Karan Chakrapani

from LLActivityPlugin import *
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

class PythonActivity(LLActivityBase):
	#initialize
	def __init__(self):
		StateList = []
		TransitionList = []
		THEFILE = "../pyscripts/test.jff"
		FILENAME = "test"
		infile = THEFILE
		count = 0
		#name of xml file in local
		
		self.getXML(infile, FILENAME, StateList, TransitionList, States, Transitions)
		self.RootInitGenerator(FILENAME, StateList, TransitionList)
		theLEN = len(StateList)
		for a in range(0, theLEN):
			theStates = StateList.pop(0)
			self.stateGenerator(FILENAME, theStates, TransitionList)		
	
	################################################################
	# Copied from sample
	def setActive( self, str):

		if self.grammarIDs.has_key(self.current_state):
			self.setCurrentGrammar(self.grammarIDs[self.current_state])
		if self.action is not None:
			self.action(self, str)
		
		self.active = True

	def processRecognition( self, gid, rid, conf, listened, rulename ):
		
		# gid: current state, rid: FSM input
		# conf: SR confidence, str: recognized string

		(self.action, self.next_state) = self.getTransition(rid, self.current_state)
		if self.action is not None:
			self.action(self, listened)

		# update status
		self.prev_state = self.current_state
		self.current_state = self.next_state
		self.next_state = None
		
		# need to change grammar
		if self.grammarIDs.has_key(self.current_state):
			newgram = self.grammarIDs[self.current_state]
		else:
			newgram = self.currentGrammarID
		
		if self.exiting is True:
			# disable current grammar
			if self.grammarIDs.has_key(self.current_state):
				self.setGrammarActive(self.grammarIDs[self.current_state], False)
			self.reset()
			return -1
		else:
			self.setCurrentGrammar(newgram)
			return newgram

	def reset (self):
		
		self.current_state = self.initial_state
		self.prev_state = None
		self.exiting = False
		self.active = False
		self.action = self.initial_action
		self.currentGrammarID = self.grammarIDs[self.initial_state]
		
	def suspend (self):
		
		# disable current SR grammar and get into suspend mode
		if self.grammarIDs.has_key(self.current_state):
			self.setGrammarActive(self.grammarIDs[self.current_state], False)
		
		self.active = False

	def resume (self):
		
		# enable current SR grammar and get back to work
		if self.grammarIDs.has_key(self.current_state):		
			self.setGrammarActive(self.grammarIDs[self.current_state], True)

	def addTransition (self, input, state, action, next_state):

		self.state_transitions[(input, state)] = (action, next_state)
		
	def getTransition (self, input, state):
		
		if self.state_transitions.has_key((input, state)):
			return self.state_transitions[(input, state)]
		else:
			return (None, state)
			
	def update (self, addedTime):
		
		# this activity just return
		return 0

	def msg_received (self, msg):
		pass
	# End copy from sample
	###################################################################
	
		#Create and add a state and all of its transitions
	def stateGenerator (self, FILENAME, States, TransitionList):
		count = 0
		tempName = FILENAME + "_" + States.name
		gramid = self.addGrammar(tempName + "_GRM")
		self.currentGrammarID = gramid
		self.grammarIDs[tempName] = gramid
		theTransLen = len(TransitionList)
		for b in range(0, theTransLen):
			Transitions = TransitionList.pop(0)
			if States.id == Transitions.fr:
				ruleid = self.addGrammarRule(gramid, tempName + "_R"+count, Transitions.keyword)
				self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
				count = count+1	
			else:
				TransitionList.append(Transitions)
	#create root/init states then call state generator
	def RootInitGenerator(self, FILENAME, StateList, TransitionList):		
		# Map (input, current_state) --> (action, next_state)
		# action is state related function assigned to it
		self.state_transitions = {}
		self.grammarIDs = {}
		self.exiting = False
		self.active = False
			
		# initial state
		self.initial_state = FILENAME + '_INI'
		self.current_state = self.initial_state
		self.action = FSM_INI_Func
		self.initial_action = FSM_INI_Func
		self.next_state = None
		self.prev_state = None
			
		# register transition to this activity from ActivityManager (top level manager)
		# use ':' as delim for multiple recognizable inputs
		self.registerTransition("test:testing")
		
		#ROOT STATE 
		count = 0;
		States = StateList.pop(0);
		tempName = FILENAME + "_ROOT"
		theTransLen = len(TransitionList)
		for b in range(0, theTransLen):
			Transitions = TransitionList.pop(0)
			if States.id == Transitions.fr:
				count = count+1	
			else:
				TransitionList.append(Transitions)
		
		#INI STATE
		count = 0;
		States = StateList.pop(0);
		tempName = FILENAME + "_INI"
		gramid = self.addGrammar(tempName + "_GRM")
		self.grammarIDs[tempName] = gramid

		theTransLen = len(TransitionList)
		for b in range(0, theTransLen):
			Transitions = TransitionList.pop(0)
			if States.id == Transitions.fr:
				ruleid = self.addGrammarRule(gramid, tempName + "_R"+count, Transitions.keyword)
				self.addTransition(ruleid, tempName, FSM_INI_Func, Transitions.to)
				count = count+1	
			else:
				TransitionList.append(Transitions)
			
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