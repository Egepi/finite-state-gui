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

count = 0
StateList = []
TransitionList = []

class States:
	def __init__(self):
		self.thisname = name
		self.thisid = id
		self.thislabel = label
		self.thisstateidle = stateidle
		
class Transitions:
	def __init__(self):
		self.thisfrom = fr
		self.thisread = read
		self.thisto = to
		self.thisresponse = response
		self.thiskeyword = keyword
  
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

for item in StateList:
	print "yes"

for item in TransitionList:
	print "okay"
	
def initialize( self ):

		# Map (input, current_state) --> (action, next_state)
		# action is state related function assigned to it
		self.state_transitions = {}
		self.grammarIDs = {}
		self.exiting = False
		self.active = False
		
		# initial state
		self.initial_state = FILENAME + '_INI'
		self.current_state = self.initial_state
		self.action = FILENAME+'_INI_Func'
		self.initial_action = FILENAME+ '+INI_Func'
		self.next_state = None
		self.prev_state = None
	    
		# register transition to this activity from ActivityManager (top level manager)
		# use ':' as delim for multiple recognizable inputs
		self.registerTransition("test:testing")
		
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
		gramid = self.addGrammar(FILENAME+"_INI_GRM")
		self.currentGrammarID = gramid
		self.grammarIDs[FILENAME+ '_INI'] = gramid
		####
		ruleid = self.addGrammarRule(gramid, "TESTA_INI_R0", "news")
		self.addTransition(ruleid, 'TESTA_INI', TESTA_NEWS_Func, 'TESTA_NEWS')
		ruleid = self.addGrammarRule(gramid, "TESTA_INI_R1", "weather")
		self.addTransition(ruleid, 'TESTA_INI', TESTA_WEATHER_Func, 'TESTA_WEATHER')
		ruleid = self.addGrammarRule(gramid, "TESTA_INI_R2", "exit")
		self.addTransition(ruleid, 'TESTA_INI', TESTA_EXIT_Func, 'TESTA_INI')
		
		
		# News state (transition to ini/exit)
		gramid = self.addGrammar("TESTA_NEWS_GRM")
		self.grammarIDs['TESTA_NEWS'] = gramid
		ruleid = self.addGrammarRule(gramid, "TESTA_NEWS_R0", "menu")
		self.addTransition(ruleid, 'TESTA_NEWS', TESTA_INI_Func, 'TESTA_INI')
		ruleid = self.addGrammarRule(gramid, "TESTA_NEWS_R1", "exit")
		self.addTransition(ruleid, 'TESTA_NEWS', TESTA_EXIT_Func, 'TESTA_INI')

		# Weather state (transition to ini/exit)
		gramid = self.addGrammar("TESTA_WEATHER_GRM")
		self.grammarIDs['TESTA_WEATHER'] = gramid
		ruleid = self.addGrammarRule(gramid, "TESTA_WEATHER_R0", "menu")
		self.addTransition(ruleid, 'TESTA_WEATHER', TESTA_INI_Func, 'TESTA_INI')
		ruleid = self.addGrammarRule(gramid, "TESTA_WEATHER_R1", "exit")
		self.addTransition(ruleid, 'TESTA_WEATHER', TESTA_EXIT_Func, 'TESTA_INI')

def stateGenerator (States, TransitionList):
		gramid = self.addGrammar(FILENAME+"_"+name+"_GRM")
		self.grammarIDs[FILENAME+"_"+name] = gramid
		for item in TransitionList:
			if States.id == item.fr:
				count = count+1
				ruleid = self.addGrammarRule(gramid, FILENAME+"_"+States.name+"R"+count, item.keyword)
				self.addTransition(ruleid, FILENAME+"_"+States.name, "Some String", item.to)
				#ruleid = self.addGrammarRule(gramid, "TESTA_NEWS_R1", "exit")
				#self.addTransition(ruleid, 'TESTA_NEWS', TESTA_EXIT_Func, 'TESTA_INI')
		