import sublime
import sublime_plugin
import sublime_api
import os
import re
import sys
import json
import subprocess
import functools
from queue import Queue
from imp import reload


__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)
_completion = None

libs_path = os.path.join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

libs_path = os.path.join(__path__, 'utils')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

# from Worker import Soxs_Worker_Thread
from sn_sublime_utils import sn_sublime
from sn_utils import sn_auto_complete
from sn_logger import logging
import sn_logger
import sn_utils
import sn_common
import sn_sublime_utils
import sn_settings, sn_sidebar, sn_open_cmd
# from soxs_parser import javascript_parser as js_parser

#######################################

auto_complete_on = True


sn = sn_sublime()
ac = sn_auto_complete()
sn_log = logging()

init_complete = False

SETTINGS_FILE = "soxsnation_util.sublime-settings"

current_position = 0;

def reload_modules():
	reload(sn_logger)
	reload(sn_utils)
	reload(sn_sublime_utils)
	reload(sn_settings)
	reload(sn_sidebar)
	reload(sn_open_cmd)
	ac = sn_auto_complete()
	sn = sn_sublime()


class ReloadModulesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		reload_modules()
		# reload(sn_logger)
		# reload(sn_utils)
		# from sn_sublime_utils import sn_utils
		# sn = sn_utils()
		# reload(sn_logger)


	def is_enabled(self):
		return True

	def is_visible(self):
		return sn_settings.developer()

def Window():
	return sublime.active_window()

class AndrewutilCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

	def is_enabled(self):
		return True

def write_status(text):
	sublime.status_message("write_status: " + text)



class TestCodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sn_log.log("Testing Code...")
		sn_log.log(str(sn_settings.get_project_data()))
		sn_log.log(str(sn.settings_init()))
		# sublime.status_message(WorkerTask.PARSE_FILE)

		# ac.file_saved(self.view.file_name())
		# init_complete = True
		# self.view.run_command('api_completions_only', True)

class SnAutoCompleteCommand(sublime_plugin.EventListener):

	def on_activated(self, view):
		if sn.settings_init() is not True:
			sn.mark_settings_init()
			sn_settings.init()

	def run(self, edit):
		sn_log.log('SnAutoCompleteCommand::RUN')

	def is_enabled(self):
		return sn_settings.sn_auto_complete_enabled()

	# def on_activated(self, view):
		# pass

	# def on_modified(self, view):
		# pass
		# view.run_command('api_completions_only', False)
		# completions = ac.completion_list()
		# view.run_command('auto_complete')

		# if sn_settings.get_project_data_item('auto_complete'):
		# 	view.run_command('api_completions_only', False)
		# 	view.run_command('auto_complete_commit_on_tab', True)
			# sn.show_auto_complete(view)

	# def on_post_save_async(self, view):
		# sublime.status_message('file saved')

		# ac.file_saved(view.file_name())

	def on_query_completions(self, view, prefix, locations):
		if sn_settings.sn_auto_complete_enabled():
			sn_log.log('on_query_completions: ' + prefix)
			# sublime.status_message('on_query_completions: ' + prefix)
			c = ac.query_complete(view, prefix, locations)
			print('Comps len: ' + str(len(c)))
			return c
		else:
			return ([], 0)

class DisplayAutoCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# sn_log.log2("DisplayAutoCompleteCommand")

		# sublime.status_message('DisplayAutoCompleteCommand')
		ac.show_auto_complete(self.view)
		# ac.test()
		# sn_log.log('DisplayAutoCompleteCommand')
		# print(str(sublime_api.view_extract_completions(self.view.id(), 'b', -1)))
 
	def is_enabled(self):
		return True

class AutoCompleteShowCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message('AutoCompleteShowCommand')
		# sn.show_auto_complete(self.view)

	def is_enabled(self):
		return True

class AutoCompleteOnCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sn.show_auto_complete(self.view)
		sn_settings.set_project_data_item('auto_complete', True)

	def is_enabled(self):
		ac = sn_settings.get_project_data_item('auto_complete')
		return not ac == True

class AutoCompleteOffCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sn.hide_auto_complete(self.view)
		sn_settings.set_project_data_item('auto_complete', False)


	def is_enabled(self):
		ac = sn_settings.get_project_data_item('auto_complete')
		return ac == True

class DebugOnCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s = sublime.load_settings(SETTINGS_FILE)
		s.set('debug_mode', True)

	def is_enabled(self):
		s = sublime.load_settings(SETTINGS_FILE)
		return not s.get('debug_mode')

class DebugOffCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s = sublime.load_settings(SETTINGS_FILE)
		s.set('debug_mode', False)

	def is_enabled(self):
		s = sublime.load_settings(SETTINGS_FILE)
		return s.get('debug_mode')
		

# GotoPythonDefinition
class GotoSoxsnationDefinitionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sn_log.log('GotoSoxsnationDefinitionCommand')
		sn_sidebar.jump_to_definition(self.view)

class OpenCmdFromFile(sublime_plugin.TextCommand):

	def run(self, edit):
		view = self.view
		sn_open_cmd.open_cmd(view.file_name())


class OpencmdCommand(sublime_plugin.WindowCommand):
	def run(self, paths = [], name = ""):
		sn_open_cmd.open_cmd(paths)

	def is_enabled(self, paths = []):
		return True

	def is_visible(self, paths =[]):
		return True



