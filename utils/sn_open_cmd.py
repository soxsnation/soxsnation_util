import sublime
import sublime_plugin
import os

from sn_logger import logging
sn_log = logging()

import sn_settings


def open_osx_terminal(path):
	sn_log.log('Opening OSX Terminal: ' + path)

def open_windows_cmd(path):
	sn_log.log('Opening Windows Command Prompt')
	os.system("start cmd /k cd " + path)

def open_linux_terminal(path):
	subprocess.Popen(["/usr/share/terminator/terminator", "--working-directory=" + path]) #/home/andrew/scratch"])

def open_os(path):
	if sublime.platform() == 'osx':
		platform = 'OSX'
		open_osx_terminal(path)
		# applescript.AppleScript('tell application "Terminal" to do script "cd"' + path).run()
		# applescript.AppleScript('launch application "Terminal"').run()
	elif sublime.platform() == 'windows':
		platform = 'Windows'			
		open_windows_cmd(path)
	else:
		platform = 'Linux'
		open_linux_terminal(path)

def open_cmd_from_file(path):
	fn = os.path.dirname(path) 
	open_os(fn)

def open_cmd(paths):
		loc = "cd C:/Users/abrown/scratch/"
		path = ''.join(paths)
		if os.path.isfile(path):
			path = os.path.dirname(path) 

		open_os(path)

		# platform = '';
		# if sublime.platform() == 'osx':
		# 	platform = 'OSX'
		# 	open_osx_terminal(path)
		# 	# applescript.AppleScript('tell application "Terminal" to do script "cd"' + path).run()
		# 	# applescript.AppleScript('launch application "Terminal"').run()
		# elif sublime.platform() == 'windows':
		# 	platform = 'Windows'			
		# 	open_windows_cmd(path)
		# else:
		# 	platform = 'Linux'
		# 	open_linux_terminal(path)



