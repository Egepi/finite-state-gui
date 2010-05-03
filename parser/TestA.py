from LLActivityPlugin import *
import pprint
import os
import xml
import sys
import re
import glob
import random

import xml.dom.minidom
from xml.dom.minidom import Node

class States:
	def __init__(self):
		#initialize values to empty or 0 values
		name = ""
		id = 0
		label = ""
		stateidle = ""
		stateidleList = []
		
class Transitions:
	def __init__(self):
		#initialize values to empty or 0 values
		fr = 0
		read = ""
		to = 0
		response = ""
		keyword = ""	
		responseList = []
###############################################################################
# Activity Class Derived from C++
###############################################################################
class PythonActivity( LLActivityBase ):

	# class initialization
	# We should use fsm xml file to generte this function
	def initialize( self ):
		StateList = []
		TransitionList = []
		THEFILE = "../pyscripts/TestA.jff"
		FILENAME = "TESTA"
		infile = THEFILE
		count = 0
		theResp = []
		exitResp = ["exiting"]
		
		# register transition to this activity from ActivityManager (top level manager)
 		# use ':' as delim for multiple recognizable inputs
		self.registerTransition("test:testing")
		
		self.getXML(infile, StateList, TransitionList)
		
		# Map (input, current_state) --> (action, next_state)
		# action is state related function assigned to it
		self.state_transitions = {}
		self.grammarIDs = {}
		self.exiting = False
		self.active = False
		
		# initialize all states and its function
		# step1: add grammar -> add default transition
		# step2: add rule -> add transition with rule id
		#  repeat step2 till all required transitions added
		
		# Initial state (initial one) to news/weather/exit
		# 1. add grammar to speech recognition engine
		# 2. store grammar id and add it to map
		# 3. add speech rules under grammar (this rule represent transition input)
		# 4. add rule to transition map
		# repeate 3~4 as many times as the number of transiton assigned to this state

		#INIT STATE
		count = 0;
		#start at the first node in the list
		States = StateList[1];
		theTransLen = len(TransitionList)
		tempName = FILENAME + "_INI"
		gramid = self.addGrammar(tempName + "_GRM")
		self.currentGrammarID = gramid
		self.grammarIDs[tempName] = gramid
		theTransLen = len(TransitionList)
		theMenuRespList = States.stateidleList
		
		# initial state initialiaztion
		self.initial_state = 'TESTA_INI'
		self.current_state = self.initial_state
		self.action = theMenuRespList
		self.initial_action = theMenuRespList
		self.next_state = None
		self.prev_state = None
		
		# adding transitions for the init state
		for b in range(0, theTransLen):
			#for each transition in transition list
			theTransition = TransitionList[b]
			for st in StateList:
				# when the transitions to element == states id element
			    if theTransition.to == st.id: 
				   newTo = FILENAME + "_" + str(st.name)
			if theTransition.fr == States.id:
				#casting things as strings 
				thing = tempName + "_R"  + str(count)
				theKey = str(theTransition.keyword)
				theResp = str(theTransition.response)
				#assigning the responselist to theresplist
				theRespList = theTransition.responseList
				theRespList = theTransition.responseList
				ruleid = self.addGrammarRule(gramid, thing, theKey)
				self.addTransition(ruleid, tempName, theRespList, newTo)
				#counter used to adding transitions 
				self.addTransition(ruleid, tempName, theRespList, newTo)		
				count = count+1	
		#adding exit
		thing = tempName + "_R"  + str(count)
		ruleid = self.addGrammarRule(gramid, thing, "exit")
		self.addTransition(ruleid, tempName, exitResp, str(FILENAME+ "_INI"))	
		count = count + 1
		#END INI STATE

		# adding all states after the init state
		theLEN = len(StateList)
		for a in range(2, theLEN):
			#theStates is the current state of StateList
			theStates = StateList[a]
			count = 0
			theTransLen = len(TransitionList)
			tempName = FILENAME + "_" + str(theStates.name)
			gramid = self.addGrammar(tempName + "_GRM")
			self.currentGrammarID = gramid
			self.grammarIDs[tempName] = gramid
			theTransLen = len(TransitionList)
			for b in range(0, theTransLen):
				theTransition = TransitionList[b]
				for st in StateList:
					if theTransition.to == st.id: 
					   newTo = FILENAME + "_" + str(st.name)
				#when the transitions from == the states id element
				if theTransition.fr == theStates.id:
					#cast elements as strings
					thing = tempName + "_R"  + str(count)
					theKey = str(theTransition.keyword)
					theResp = str(theTransition.response)
					#assign the current responselist to theresplist
					theRespList = theTransition.responseList
					theRespList = theTransition.responseList
					ruleid = self.addGrammarRule(gramid, thing, theKey)
					self.addTransition(ruleid, tempName, theRespList, newTo)
					count = count+1	
			#adding init and exit 		
			thing = tempName + "_R"  + str(count)
			ruleid = self.addGrammarRule(gramid, thing, "menu")
			self.addTransition(ruleid, tempName, theMenuRespList, str(FILENAME+ "_INI"))
			count = count+1
			thing = tempName + "_R"  + str(count)
			ruleid = self.addGrammarRule(gramid, thing, "exit")
			self.addTransition(ruleid, tempName, exitResp, str(FILENAME+ "_INI"))
			count = count+1
		
	def setActive( self, str):

		if self.grammarIDs.has_key(self.current_state):
			self.setCurrentGrammar(self.grammarIDs[self.current_state])
		if self.action is not None:
			#random output for the menu response
			randInt2 = random.randint(0, (len(self.action)-1))
			menuResponse = self.action[randInt2]
			self.speak(menuResponse)
		
		self.active = True

	def processRecognition( self, gid, rid, conf, listened, rulename):
		
		# gid: current state, rid: FSM input
		# conf: SR confidence, str: recognized string
		(self.action, self.next_state) = self.getTransition(rid, self.current_state)
		if self.action is not None:
			# random output
			randInt = random.randint(0, (len(self.action)-1))
			myResponse = self.action[randInt]
		 	self.speak(myResponse)
			
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

	#getting the xml file
	def getXML(self, infile, StateList, TransitionList):
		# file input
		try:                          
			doc = xml.dom.minidom.parse(infile)
		except IOError:               # catch IOError and deriving exceptions
			print "Could not open\n"
			os._exit(99)
		
	    #initializing the elements within each state tag
		for node in doc.getElementsByTagName("state"):
			id = node.getAttribute("id")
			name = node.getAttribute("name")
			stateidle = node.getElementsByTagName("stateIdleResp")
			label = node.getElementsByTagName("label")
			stateidleList = []
			x = States()
			x.id = id
			x.name = name
			# checks nodes for stateidle responses
			for node2 in stateidle:
				stateidle = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					stateidle += node3.data	
					x.stateidle = stateidle
					try:
						#parsing state idle transitions into a list
						strStateIdle = str(stateidle)
						x.stateidleList = strStateIdle.split(":")
					except AttributeError:
						print("")	
					try:
						strStateIdle = str(stateidle)
						x.stateidleList = strStateIdle.split(":")
					except AttributeError:
						print("")	
			#save to state object put into lists
			for node2 in label:
				label = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					label += node3.data	
					x.label = label
			#appends the state to the state list		
			StateList.append(x)
		#parsing for all elements in transition	  
		for node in doc.getElementsByTagName("transition"):
			fr = node.getElementsByTagName("from")
			read = node.getElementsByTagName("read")
			to = node.getElementsByTagName("to")
			response = node.getElementsByTagName("response")
			keyword = node.getElementsByTagName("keyword")
			responseList = []
			y = Transitions()
			for node2 in fr:
				fr = ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					fr += node3.data	  
					#assigns the fr data to the transition
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
					try:
						# parses the responses into a list
						strResp = str(response)
						y.responseList = strResp.split(":")
					except AttributeError:
						print("")						
					try:
						strResp = str(response)
						y.responseList = strResp.split(":")
					except AttributeError:
						print("")						
			for node2 in keyword:
				keyword	= ""
			for node3 in node2.childNodes:
				if node3.nodeType == Node.TEXT_NODE:
					keyword += node3.data
					y.keyword = keyword
			#appends the transition to the TransitionList		
			TransitionList.append(y)