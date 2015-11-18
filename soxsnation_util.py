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

# from Worker import Soxs_Worker_Thread
from sn_sublime_utils import sn_sublime_utils
from sn_utils import sn_auto_complete
from sn_logger import logging
import sn_logger
import sn_utils
import sn_common
# from soxs_parser import javascript_parser as js_parser

#######################################

auto_complete_on = True


sn = sn_sublime_utils()
ac = sn_auto_complete()
sn_log = logging()

init_complete = False

SETTINGS_FILE = "soxsnation_util.sublime-settings"

current_position = 0;

def reload_modules():
	reload(sn_logger)
	reload(sn_utils)
	ac = sn_auto_complete()
	# reload(sn_sublime_utils)

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

def _set_current_completion(completion):
  global _completion
  _completion = completion

def _get_current_completion():
  global _completion
  return _completion

def Window():
	return sublime.active_window()

def debug():
	s = sublime.load_settings(SETTINGS_FILE)
	debug = s.get('debug_mode')
	return debug

class AndrewutilCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

	def is_enabled(self):
		return True

def write_status(text):
	sublime.status_message("write_status: " + text)

def test_fun():
	sublime.status_message('Utils work!!')
	sn.set_project_data_item('auto_complete', False)

def test_parse(view):
	reg = sublime.Region(0, view.size())
	# content = view.substr(reg)
	# javascript_parse_functions(content)

	

def test_init_autocomplete():
	folder = sn.get_project_data_item('folders')[0]['path']
	# sublime.status_message(str(folder))
	
	num_comp = ac.parse_project(folder)
	sublime.status_message('Found ' + str(num_comp) + ' completions: ')
	file_name = '/Users/Andrew/Documents/soxsnation_fantasy_list.json'
	
	# comps = ac.full_list()
	# sublime.status_message(str(num_comp) + ' completions are unique ')
	# with open(file_name, 'w') as outfile:
	# 	json.dump(comps, outfile)


class TestCodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message("Testing Code...")
		# sublime.status_message(WorkerTask.PARSE_FILE)
		# test_init_autocomplete()

		ac.file_saved(self.view.file_name())
		init_complete = True
		self.view.run_command('api_completions_only', True)

		# test_fun()
		# test_parse(Window().active_view())

		# for x in range(3):
		# 	worker = Soxs_Worker(queue)
		# 	worker.daemon = True
		# 	worker.start()

		# for x in range(20):
		# 	queue.put("Item: " + str(x))

		# queue.join()
		# sublime.status_message("Testing Code...Complete")

def make_completion(trigger, contents):
	return (trigger, contents)

def completes():
	ac = []
	ac.append(make_completion('post_playsss', 'post_playsss_value'))
	ac.append(make_completion('post_game_plays', 'post_game_plays_value'))
	ac.append(make_completion('post_game_data', 'post_game_data_value'))
	return ac

def completes2(view):
	reg = sublime.Region(0, view.size())
	s = view.substr(reg)
	funs = javascript_parse_functions(s)
	ac = []
	for f in funs:
		ac.append(make_completion(f['name'], f['name']))

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

def show_completions(view, prefix):
	sublime.status_message('show_completions: ' + str(auto_complete_on))
	if auto_complete_on:

		# if sn.get_project_data_item('auto_complete') and init_complete:
			# ac = completes2(view)
			# sublime.status_message(str(ac))
			# return (ac, sublime.INHIBIT_WORD_COMPLETIONS)
			# return (ac, sublime.INHIBIT_EXPLICIT_COMPLETIONS)
		# view.run_command('api_completions_only', False)
		# view.run_command('auto_complete')
		
		# completions = ac.completion_list()
		completions = [{"test":"test"},{"testing":"testing"}]
		# view.run_command('auto_complete')

		# return (completions, sublime.INHIBIT_WORD_COMPLETIONS)

class SnAutoCompleteCommand(sublime_plugin.EventListener):

	# def on_activated(self, view):
		# pass

	# def on_modified(self, view):
		# pass
		# view.run_command('api_completions_only', False)
		# completions = ac.completion_list()
		# view.run_command('auto_complete')

		# if sn.get_project_data_item('auto_complete'):
		# 	view.run_command('api_completions_only', False)
		# 	view.run_command('auto_complete_commit_on_tab', True)
			# sn.show_auto_complete(view)


	# def on_post_save_async(self, view):
		# sublime.status_message('file saved')

		# ac.file_saved(view.file_name())



	def on_query_completions(self, view, prefix, locations):
		sn_log.log('on_query_completions: ' + prefix)
		# sublime.status_message('on_query_completions: ' + prefix)
		# show_completions(view, prefix)
		c = ac.query_complete(view, prefix, locations)
		print('Comps len: ' + str(len(c)))
		return c

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
		sn.set_project_data_item('auto_complete', True)

	def is_enabled(self):
		ac = sn.get_project_data_item('auto_complete')
		return not ac == True

class AutoCompleteOffCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sn.hide_auto_complete(self.view)
		sn.set_project_data_item('auto_complete', False)


	def is_enabled(self):
		ac = sn.get_project_data_item('auto_complete')
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

def get_results(loc, result):
	# sublime.message_dialog('function index was selected: ' + str(len(loc)))
	if result > -1:
		jump_to_loc(loc[result])

def set_cursor_position(view, position):
	# sublime.message_dialog('set_cursor_position: ' + str(position))
	# view.show_at_center(position)
	# pos = view.sel()
	view.sel().clear()
	view.sel().add(sublime.Region(position))
	view.show_at_center(position)

def jump_to_loc(loc):
	loc_str = str(loc)
	file_loc = str(loc[0])
	if debug():
		sublime.message_dialog('Found function here: ' + str(loc_str))

	view_list = Window().views()
	found_view = False
	for i in range(0, len(view_list)-1):
		if file_loc == view_list[i].file_name():
			found_view = True
			func_loc = Window().get_view_index(view_list[i])

			if Window().active_group() == func_loc[0]:
				Window().focus_view(view_list[i])
				text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
				set_cursor_position(view_list[i], text_pt)
			else:
				Window().set_view_index(view_list[i], func_loc[0], func_loc[1])
				text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
				set_cursor_position(view_list[i], text_pt)
	if not found_view:
		Window().open_file(file_loc)
		text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
		set_cursor_position(view_list[i], text_pt)

def jump_to_definition(self):
	view = self.view

	region = view.sel()[-1]
	region = view.word(region)
	content = view.substr(region)
	if debug():
		sublime.message_dialog('function name: ' + str(content))

	loc = Window().lookup_symbol_in_index(content)
	if debug():
		sublime.message_dialog('loc: ' + str(loc))

	if len(loc) == 0:
		sublime.message_dialog('function not found: ' + str(content))
	elif len(loc) > 1:
		loc_list = []
		for i in range(0, len(loc)):
			if not 'node_modules' in loc[i][1]:
				v = []
				v.append(loc[i][1])
				v.append('Line: ' + str(loc[i][2][0]))
				loc_list.append(v)
		if len(loc_list) == 0:
			sublime.message_dialog('function not found: ' + str(content))
		else:
			Window().show_quick_panel(loc_list, functools.partial(get_results, loc))
	else:
		jump_to_loc(loc[0])
		

# GotoPythonDefinition
class GotoSoxsnationDefinitionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# sublime.status_message('GotoSoxsnationDefinitionCommand clicked()')
		jump_to_definition(self)
		# Window().show_quick_panel([yes, no], functools.partial(self.get_results))


	# def get_results(self, result):
	# 	sublime.message_dialog('function index was selected: ' + str(result))




class OpencmdCommand(sublime_plugin.WindowCommand):
	def run(self, paths = [], name = ""):
		loc = "cd C:/Users/abrown/scratch/"
		path = ''.join(paths)
		# sublime.message_dialog(path)
		# os.system("start cmd /k " + loc)
		# sublime.status_message('Here is the paths:')
		# sublime.status_message(sublime.active_window().folders())

		platform = '';
		if sublime.platform() == 'osx':
			platform = 'OSX'
			sublime.status_message('OSX')
			# applescript.AppleScript('tell application "Terminal" to do script "cd"' + path).run()
			# applescript.AppleScript('launch application "Terminal"').run()
		elif sublime.platform() == 'windows':
			platform = 'Windows'			
			# sublime.message_dialog(path)
			os.system("start cmd /k cd " + path)
		else:
			platform = 'Linux'
			subprocess.Popen(["/usr/share/terminator/terminator", "--working-directory=" + path]) #/home/andrew/scratch"])



	def is_enabled(self, paths = []):
		return True

	def is_visible(self, paths =[]):
		return True



