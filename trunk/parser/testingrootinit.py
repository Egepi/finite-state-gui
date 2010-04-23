# FSMGUI XML ('jff') to Python Parser
# Authors: Jennifer Kinahan & Karan Chakrapani

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
		
class Transitions:
	def __init__(self):
		#initialize values to empty or 0 values
		fr = 0
		read = ""
		to = 0
		response = ""
		keyword = ""	

StateList = []
TransitionList = []
FILENAME = ""	
infile = "template.jff"

def RootInitGenerator(self, StateList, TranistionList):		
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
	tempName = FILENAME + "_" + States.label
	gramid = self.addGrammar(tempName+"_GRM")
	self.grammarIDs[tempName] = gramid
	print tempName
	for Transitions in TransitionList:
		if States.id == Transitions.fr:
			ruleid = self.addGrammarRule(gramid, tempName+"_R"+count, Transitions.keyword)
			self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
			Transitions.remove(Transitions);
			count = count + 1
	
	#INI STATE
	count = 0;
	States = StateList.pop(1);
	tempName = FILENAME + "_" + States.label
	gramid = self.addGrammar(tempName + "_GRM")
	self.grammarIDs[tempName] = gramid

	for Transitions in TransitionList:
		if States.id == Transitions.fr:
			ruleid = self.addGrammarRule(gramid, tempName + "_R" + count, Transitions.keyword)
			self.addTransition(ruleid, tempName, FSM_TEST_Func, Transitions.to)
			Transitions.remove(Transitions);
			count = count+1 
	
	for States in StateList:
			statesGenerator(self, States, TransitionList)
	if not States:
		print "end of StatesList"
		os._exit(99)