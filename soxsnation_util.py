import sublime
import sublime_plugin
import os
import re
import sys
import subprocess
import functools

SETTINGS_FILE = "soxsnation_util.sublime-settings"

current_position = 0;

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
		
class AutoCompleteCommand(sublime_plugin.EventListener):
	def on_modified(self, view):
		region = view.sel()[-1]
		region = view.word(region)
		content = view.substr(region)
		sublime.status_message('auto complete: ' + content)

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



