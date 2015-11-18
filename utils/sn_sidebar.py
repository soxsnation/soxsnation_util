import sublime
import sublime_plugin
import functools

from sn_logger import logging
sn_log = logging()

import sn_settings

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
	if sn_settings.debug_mode():
		sn_log.log('Found function here: ' + str(loc_str))

	view_list = sublime.active_window().views()
	found_view = False
	for i in range(0, len(view_list)-1):
		if file_loc == view_list[i].file_name():
			found_view = True
			func_loc = sublime.active_window().get_view_index(view_list[i])

			if sublime.active_window().active_group() == func_loc[0]:
				sublime.active_window().focus_view(view_list[i])
				text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
				set_cursor_position(view_list[i], text_pt)
			else:
				sublime.active_window().set_view_index(view_list[i], func_loc[0], func_loc[1])
				text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
				set_cursor_position(view_list[i], text_pt)
	if not found_view:
		sublime.active_window().open_file(file_loc)
		text_pt = view_list[i].text_point(loc[2][0]-1, loc[2][1]-1)
		set_cursor_position(view_list[i], text_pt)

def jump_to_definition(view):

	region = view.sel()[-1]
	region = view.word(region)
	content = view.substr(region)
	# if sn_settings.debug_mode():
	sn_log.log('function name: ' + str(content))

	loc = sublime.active_window().lookup_symbol_in_index(content)
	if sn_settings.debug_mode():
		sn_log.log('loc: ' + str(loc))

	if len(loc) == 0:
		sn_log.log('function not found: ' + str(content))
	elif len(loc) > 1:
		loc_list = []
		for i in range(0, len(loc)):
			if not 'node_modules' in loc[i][1]:
				v = []
				v.append(loc[i][1])
				v.append('Line: ' + str(loc[i][2][0]))
				loc_list.append(v)
		if len(loc_list) == 0:
			sn_log.log('function not found: ' + str(content))
		else:
			sublime.active_window().show_quick_panel(loc_list, functools.partial(get_results, loc))
	else:
		jump_to_loc(loc[0])