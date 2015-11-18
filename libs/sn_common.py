# import sublime
# import sublime_plugin
import os
import sys
import time
from queue import Queue
# from enum import Enum

# class WorkerTask(Enum):
# 	ParseFile = 1
# 	ParseDirectory = 2

def enum(**named_values):
	return type('Enum', (), named_values)

# def init():
# 	global WorkerTask
	
WorkerTask =enum(PARSE_FILE='parse_file', PARSE_DIRECTORY='parse_directory')
CompletionType = enum(FUNCTION='function', VARIABLE='variable')


def make_completion(text, vars, loc, type):
	c = {}
	c['text'] = text
	c['value'] = text
	c['vars'] = vars
	c['type'] = type
	c['loc'] = loc
	return c

