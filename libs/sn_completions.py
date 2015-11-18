import os
# import os.path
import sys
import json

class completion_list(object):
	def __init__(self):
		self.project = "project"
		self.completion_list = []

	def add_completion_list(self, comp_list):
		for c in comp_list:
			self.add_completion(c)

	def add_completion(self, comp):
		if not self.completion_exists(comp):
			self.completion_list.append(comp)

	def compare(self, comp1, comp2):
		if comp1['text'] != comp2['text']:
			return False
		if comp1['value'] != comp2['value']:
			return False
		if comp1['loc'] != comp2['loc']:
			return False
		if comp1['vars'] != comp2['vars']:
			return False
		return True

	def completion_exists(self, comp):
		for c in self.completion_list:
			if self.compare(c, comp):
				return True
		return False

	def full_list(self):
		return self.completion_list

	def completions(self):
		cl = []
		for c in self.completion_list:
			it = (c['text'], c['value'])
			if not it in cl:
				cl.append(it)
		return cl