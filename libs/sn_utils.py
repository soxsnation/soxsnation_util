import sublime
import sublime_plugin
import sublime_api
import os
# import os.path
import sys
import json
from queue import Queue
import functools

from soxs_parser import javascript_parser as js_parser
from soxs_parser import python_parser as python_parser
from sn_completions import completion_list

from Worker import Soxs_Worker_Thread
import sn_common as sn
from sn_logger import logging
sn_log = logging()

def file_extenstion(filename):
	return filename[filename.rfind('.'):]

def walk_dir(dir, ext):
	file_list = []
	print('walk_dir: ' + ext)
	for root, subdirs, files in os.walk(dir):
		for fname in files:
			if (file_extenstion(os.path.join(root, fname)) == ext):
				file_list.append(os.path.join(root, fname))
	return file_list

# class completion_list(object):
# 	def __init__(self):
# 		self.project = "project"
# 		self.completion_list = []

# 	def add_completion(self, comp):
# 		if not self.completion_exists(comp):
# 			self.completion_list.append(comp)

# 	def compare(self, comp1, comp2):
# 		if comp1['text'] != comp2['text']:
# 			return False
# 		if comp1['value'] != comp2['value']:
# 			return False
# 		if comp1['loc'] != comp2['loc']:
# 			return False
# 		if comp1['vars'] != comp2['vars']:
# 			return False
# 		return True

# 	def completion_exists(self, comp):
# 		for c in self.completion_list:
# 			if self.compare(c, comp):
# 				return True
# 		return False

# 	def full_list(self):
# 		return self.completion_list

# 	def completions(self):
# 		cl = []
# 		for c in self.completion_list:
# 			it = (c['text'], c['value'])
# 			if not it in cl:
# 				cl.append(it)
# 		return cl
def make_completion(trigger, contents):
	return (trigger, contents)
	
def completes():
	ac = []
	ac.append(make_completion('post_playsss', 'post_playsss_value'))
	ac.append(make_completion('post_game_plays', 'post_game_plays_value'))
	ac.append(make_completion('post_game_data', 'post_game_data_value'))
	return ac

def show_ac(view):
	def _show_auto_complete():
		view.run_command('auto_complete', {
			'disable_auto_insert': True,
			'api_completions_only': True,
			'next_completion_if_showing': False,
			'auto_complete_commit_on_tab': True
			})
	sublime.set_timeout(_show_auto_complete, 0)


class sn_auto_complete(object):

	def __init__(self):
		self.project = "project"
		self.sn_comps = completion_list()
		self.last_completion = ""

	##########################################################################################
    # Common
    ##########################################################################################

	def languages(self):
		l = []
		l.append('javascript')
		l.append('python')
		return l

	# def completion_types(self):
	# 	ct = []
	# 	ct.append('function')
	# 	ct.append('variable')

	# def make_completion(self, text, value, vars, type, location, ud):
	# 	completion = {}
	# 	completion['text'] = text;
	# 	completion['value'] = value;
	# 	completion['vars'] = vars;
	# 	completion['type'] = type;
	# 	completion['loc'] = location;
	# 	completion['userdefined'] = ud;
	# 	self.completion_list.add_completion(completion)

	##########################################################################################
    # Actions
    ##########################################################################################

	def write_out_completions(self):
		file_name = '/Users/Andrew/Library/Application Support/Sublime Text 3/Packages/soxsnation_util/logs/completions.json'
		with open(file_name, 'w') as outfile:
			json.dump(self.sn_comps.full_list(), outfile)

	def thread_return(self, data):
		self.sn_comps.add_completion_list(data)
		# sublime.status_message(str(data))
		self.write_out_completions()

	def make_file_task(self, file_name):
		t = {}
		t["task"] = sn.WorkerTask.PARSE_FILE
		t["file"] = file_name
		t['cb'] = functools.partial(self.thread_return)
		return t

	def make_dir_task(self, dir_name):
		t = {}
		t["task"] = sn.WorkerTask.PARSE_DIRECTORY
		t["dir"] = dir_name
		t['cb'] = functools.partial(self.thread_return)
		return t

	def file_saved(self, file_name):
		q = Queue()
		q.put(self.make_file_task(file_name))
		Soxs_Worker_Thread(q).start()

	def completion_list(self):
		return self.sn_comps.completions()

	def show_auto_complete(self, view):
		sublime.status_message('ac.show_auto_complete')
		view.run_command('api_completions_only', False)
		view.run_command('auto_complete')

	def test(self):
		sn_log.log('ac.test')
		# sublime.status_message('ac.test')

	def query_complete(self, view, prefix, location):
		sn_log.log('query_complete: ' + prefix)
		# completions = [{"test":"test"},{"testing":"testing"},{"alpha":"alpha"},{"beta":"beta"}]
		completions = [["test","test"],["testing","testing"],["alpha","alpha"],["beta","beta","beta.js"]]
		sn_log.data(completions)
		return (completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS)


	# def get_function_defs(self, jp, dirname):
	# 	file_list = walk_dir(dirname, jp.valid_extenstions()[0])
	# 	for fname in file_list:
	# 		with open(fname) as f:
	# 			content = f.read()
	# 			print(fname + ' has ' + str(len(content)) + ' characters')
	# 			fl = jp.javascript_parse_functions(content)
	# 			for fun in fl:
	# 					self.make_completion(fun['name'], fun['name'], fun['vars'], 'function', fname, True)


	# def parse_project(self, dirname):
	# 	jp = js_parser()
	# 	dirname2 = '/Users/Andrew/Documents/scratch/javascript_test/'
	# 	self.get_function_defs(jp, dirname2)
	# 	return len(self.completion_list.completions())

	# def completions(self):
	# 	return self.completion_list.completions()

	# def full_list(self):
	# 	return self.completion_list.full_list()

	# def test_javascript(self):
	# 	jp = js_parser()
	# 	folder = '/Users/Andrew/Documents/scratch/javascript_test/'
	# 	print(folder)
	# 	fun_list = []
		









