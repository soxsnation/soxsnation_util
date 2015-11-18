import sublime
import sublime_plugin
import os
import sys
import time

# from queue import Queue
import threading
import sn_common as sn

from soxs_parser import javascript_parser as js_parser
from soxs_parser import python_parser as python_parser

jp = js_parser()


class Soxs_Worker_Thread(threading.Thread):
	def __init__(self, q):
		self.q = q
		self.completions = []
		threading.Thread.__init__(self)

		# self.file = file
		# self.task = task
		

	def make_completion(self, text, value, vars, type, location, ud):
		completion = {}
		completion['text'] = text;
		completion['value'] = value;
		completion['vars'] = vars;
		completion['type'] = type;
		completion['loc'] = location;
		completion['userdefined'] = ud;
		return completion

	def run(self):
		task = self.q.get()
		sublime.status_message('Starting Soxs_Worker_Thread...' + task['task'])
		if task['task'] == sn.WorkerTask.PARSE_FILE and os.path.isfile(task['file']):
			fl = jp.javascript_parse_file(task['file'])
			comps = []
			for c in fl:
				comp = sn.make_completion(c['name'], c['vars'], task['file'], sn.CompletionType.FUNCTION)
				comps.append(comp)
			task['cb'](comps)
		# elif task['task'] == sn.WorkerTask.PARSE_DIRECTORY and os.path.isdir(self.file):
		# 	file_list = self.walk_dir(task['dir'], jp.valid_extenstions()[0])
		# 		for fname in file_list:
		# 			fl = jp.javascript_parse_file(self.file)


		



	# def completions(self):
	# 	return ["completions", "completions2"]

	# def parse_for_functions(self, fl):
	# 	completion_list = []
	# 	for fun in fl:
	# 		completion_list.append(self.make_completion(fun['name'], fun['name'], fun['vars'], 'function', fname, True))
	# 	return completion_list

	# def file_extenstion(self, filename):
	# 	return filename[filename.rfind('.'):]

	# def walk_dir(self, dir):
	# 	file_list = []
	# 	for root, subdirs, files in os.walk(dir):
	# 		for fname in files:
	# 			if (file_extenstion(os.path.join(root, fname)) == jp.valid_extenstions()[0]):
	# 				file_list.append(os.path.join(root, fname))
	# 	return file_list

	# def update_completions_data(self, completion_list):
	# 	comps = sublime.active_window().project_data()['sn_completions']
	# 	for comp in comps:



