import sublime
import sublime_plugin
import os
import sys
import json

SETTINGS_FILE = "soxsnation_util.sublime-settings"

def soxsnation_project_settings():
	sn_list = []
	sn_list.append({"name":"developer", "value" : False})
	return sn_list

def soxsnation_sublime_settings():
	sn_list = []
	sn_list.append({"name":"debug_mode", "value" : False})
	sn_list.append({"name":"auto_complete", "value" : False})
	sn_list.append({"name":"developer", "value" : False})
	return sn_list

def Window():
    return sublime.active_window()

def init():
	print('sn_settings::init()')
	s = sublime.load_settings(SETTINGS_FILE)
	for item in soxsnation_sublime_settings():
		if not s.has(item['name']):
			s.set(item['name'], item['value'])

	pd = get_project_data()
	for item in soxsnation_project_settings():
		if item['name'] not in pd:
			pd[item['name']] = item['value']
	set_project_data(pd)


##########################################################################################
# Project Specific Settings
##########################################################################################

def get_project_data():
    return Window().project_data()

def get_project_data_item(item):
	pd = Window().project_data()
	if item in pd:
		return pd[item]
	else :
		return {}

def set_project_data(data):
    Window().set_project_data(data)

def set_project_data_item(item, data):
	pd = Window().project_data()
	pd[item] = data
	Window().set_project_data(pd)


##########################################################################################
# Sublime Settings
##########################################################################################

def debug_mode():
	s = sublime.load_settings(SETTINGS_FILE)
	debug = s.get('debug_mode', False)
	return debug

def developer():
	s = sublime.load_settings(SETTINGS_FILE)
	dev = s.get('developer', False)
	# print('sn_setting::developer: ' + str(dev))
	return dev

def sn_auto_complete_enabled():
	if get_project_data_item('auto_complete'):
		s = sublime.load_settings(SETTINGS_FILE)
		ac = s.get('auto_complete', False)
		print('sn_setting::an_auto_complete_enabled: ' + str(ac) + '  ' + str(get_project_data_item('auto_complete')))
		return ac
	else:
		print('sn_setting::an_auto_complete_enabled: Turned off in the project')
		return False
	
