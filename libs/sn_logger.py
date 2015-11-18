import sublime
import sublime_plugin
import os
import sys
import datetime





class logging(object):

	def __init__(self):
		self.logging_on = True
		self.log_file_enabled = True

	def turn_log_file_on(self):
		self.log_file_enabled = True

	def turn_log_file_off(self):
		self.log_file_enabled = False

	def log_file_name(self):
		d = datetime.datetime.now()
		filename = str(d.year) + str(d.month) + str(d.day) + '_log.txt' 
		return "/Users/Andrew/Library/Application Support/Sublime Text 3/Packages/soxsnation_util/logs/" + filename

	def date_time_stamp(self):
		d = datetime.datetime.now()
		return "[" + str(d) + "]"


	def log(self, message):
		print(self.date_time_stamp() + ' -- ' + message)
		if self.logging_on:
			sublime.status_message(message)
		if self.log_file_enabled:
			with open(self.log_file_name(), "a") as myfile:
				myfile.write(self.date_time_stamp() + ' -- ' + message + '\n')

	def data(self, data):
		print(str(data))
		if self.log_file_enabled:
			with open(self.log_file_name(), "a") as myfile:
				myfile.write(self.date_time_stamp() + ' -- ' + str(data) + '\n')