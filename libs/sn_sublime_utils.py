import sublime
import sublime_plugin
import os
import sys
import json


class sn_sublime(object):
	def __init__(self):
		self.project = "project"
		self.settings_initialized = False

	def status(self, message):
		sublime.status_message(message)

	def Window(self):
		return sublime.active_window()	
		
	def settings_init(self):
		return self.settings_initialized

	def mark_settings_init(self):
		self.settings_initialized = True

	def hide_auto_complete(self, view):
		view.run_command('hide_auto_complete')

	def show_auto_complete(self, view):
		view.run_command('auto_complete')

	def debug_data(self, data):
		file_name = '/Users/Andrew/Documents/debug.json'
		f = open(file_name, 'w')
		f.write(str(data))