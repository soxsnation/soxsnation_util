# import sublime
# import sublime_plugin
import os.path
import sys

class parser(object):
	def __init__(self):
		self.language = "javascript"

class javascript_parser(object):

	def __init__(self):
		self.language = "javascript"
		self.extenstions = []
		self.extenstions.append('.js')

	def valid_extenstions(self):
		return self.extenstions

	def exclude_directories(self):
		dirs = []
		dirs.append('node_modules')
		return dirs

	def javascript_parse_function_vars(self, s):
		vl = s.split(',')
		var_list = []
		for v in vl:
			var_list.append(v.strip())
		return var_list

	def javascript_parse_functions(self, s):
		lines = s.split('\n')
		fmt_str = ''
		fun_list = []
		for line in lines:
			l = line.strip()
			if (len(l) > 0 and l[0:2] != '//'):
				fmt_str += l
				if (l[0:8] == 'function'):
					fun_def = {}
					fun_name = l[l.find(' ', 8)+1:l.find('(',9)]
					if len(fun_name) > 1:
						fun_def['name'] = fun_name.strip()
						fun_def['vars'] = self.javascript_parse_function_vars(l[l.find('(', 9)+1:l.find(')',9)])
						fun_list.append(fun_def)
		return fun_list

	def javascript_parse_file(self, file):
		with open(file) as f:
			content = f.read()
			return self.javascript_parse_functions(content)


class python_parser(object):
	def __init__(self):
		self.language = "python"