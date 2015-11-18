import sublime
import sublime_plugin
import os
import sys
import json


class sn_sublime_utils(object):
	def __init__(self):
		self.project = "project"

	def status(self, message):
		sublime.status_message(message)

	def Window(self):
		return sublime.active_window()	

	def get_project_data(self):
		return self.Window().project_data()

	def get_project_data_item(self, item):
		pd = self.Window().project_data()
		if item in pd:
			return pd[item]
		else:
			return {}

	def set_project_data(self, data):
		self.Window().set_project_data(data)

	def set_project_data_item(self, item, data):
		pd = self.Window().project_data()
		pd[item] = data
		self.Window().set_project_data(pd)

	def hide_auto_complete(self, view):
		view.run_command('hide_auto_complete')

	def show_auto_complete(self, view):
		view.run_command('auto_complete')

	def debug_data(self, data):
		file_name = '/Users/Andrew/Documents/debug.json'
		f = open(file_name, 'w')
		f.write(str(data))