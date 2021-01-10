import copy
from typing import *


def addquotes(in_str : str):
	return '\"%s\"' % in_str

"""
 #######  ########  ####  ######  ########
##     ## ##     ##  ##  ##    ##    ##
##     ## ##     ##  ##  ##          ##
##     ## ##     ##  ##  ##          ##
##     ## ##     ##  ##  ##          ##
##     ## ##     ##  ##  ##    ##    ##
 #######  ########  ####  ######     ##
"""

# objects from dicts
class ObjectDict(object):
	def __init__(self, data):
		"""ObjectDict

		allows accessing elements of a dictionary as `object.key` instead of `object['key']`

		why is this useful when you can just dump it into `object.__dict__` ?
		primarily because doing that will make copying your dict rather difficult without ending up with somewhat of a mess.
		
		"""
		self.__dict__['_data'] = copy.deepcopy(data)

		for key,val in self._data.items():
			if isinstance(val, dict):
				self._data[key] = ObjectDict(val)
	
	def __getattr__ (self, name : str) -> Any:
		if name in self._data:
			return self._data[name]
		else:
			raise KeyError()
	
	def __setattr__(self, name : str, value : Any) -> None:
		if name in self._data:
			self._data[name] = value
		else:
			raise KeyError()

	def __getitem__(self, key : str) -> Any:
		return self._data[key]
	
	def __setitem__(self, key : str, value : Any) -> None:
		self._data[key] = value

	def __str__(self):
		return str(self.asDict())

	def asDict(self):
		return {
			k : (v.asDict() if isinstance(v, ObjectDict) else v)
			for k,v in self._data.items()
		}

	@staticmethod
	def from_args(**kwargs):
		return ObjectDict(kwargs)




def gen_instance_ctor(
		data : dict,
		filename : str = None,
		use_as_defaults : bool = False,
		in_as_dict : bool = True,
		# make_dict_objdict : bool = True,
		# gen_typehints = False,
		dName : str = '_data',
	):
	"""generate a constructor for a class that takes in a dict.

	given a dict `data`, generates (most) of the constructor for an object that
	takes in some dictionary with the same structure as `data`, and uses it to 
	
	this has very limited use cases, and is only for very lazy people such as myself.
	essentially a way to hard-convert dicts to objects.
	you should probably just use `ObjectDict._data.update()`

	Args:
		data (dict): input data
		filename (str, optional): filename to print to. Defaults to None (printing to console).
		use_as_defaults (bool, optional): use the values in `data` as default values for the constructor. Defaults to False.
		in_as_dict (bool, optional): whether the input to the ctor is a dict or keyword values. Defaults to True.
		dName (str, optional): name of the keyword argument, if `in_as_dict` is True. Defaults to '_data'.
	"""
	# output lists of lines
	output_args = []
	output_assign = []

	
	# loop over all items
	if in_as_dict:
		# print either as a dict
		output_args.append('%s = {' % dName)
		for key,val in data.items():
			if use_as_defaults:
				output_args.append(
					'\t\'%s\' : %s,' 
					% (
						key,
						(
							addquotes(str(val))
							if isinstance(val,str) 
							else str(val)
						),
					)
				)
			else:
				output_args.append(
					"\t\'%s\' : None," % key
				)
			output_assign.append("self.%s = %s[\'%s\']" % (key, dName, key))
		output_args.append('}')

	else:
		# or as keywords in the args
		for key,val in data.items():
			output_args.append(
				('%s' % key)
				+ (' = %s,' % str(val))
					if use_as_defaults 
					else ','
			)
			output_assign.append('self.%s = %s' % (key, key))

		


	if filename is not None:
		f = open(filename, 'w')
	else:
		f = None


	print('def __init__(\n\t\tself,', file=f)
	for line in output_args:
		print('\t\t' + line, file=f)
	print('\t) -> None:\n', file=f)
	for line in output_assign:
		print('\t' + line, file=f)


	if f is not None:
		f.flush()
		f.close()




"""
########  ####  ######  ########  #######
##     ##  ##  ##    ##    ##    ##     ##
##     ##  ##  ##          ##    ##     ##
##     ##  ##  ##          ##    ##     ##
##     ##  ##  ##          ##    ##     ##
##     ##  ##  ##    ##    ##    ##     ##
########  ####  ######     ##     #######
"""

# special dicts from objects
class dictObj(dict):

	def __init__(self, d, mode = dict):
		'''
		create a dictionary, given an object. this is pretty much useless
		'''
		if isinstance(mode, dict):
			newDict = d
		elif isinstance(mode, object):
			newDict = d.__dict__
		else:
			raise KeyError('invalid mode for `dictObj` ctor:\t%s' % str(mode))
		
		for key,val in newDict.items():
			self[key] = copy.deepcopy(val)

	def __getattr__(self, name):
		if name in self:
			return self[name]
		else:
			raise AttributeError('invalid attribute:\t%s' % name)

	def __setattr__(self, name, value):
		self[name] = value

	def __delattr__(self, name):
		if name in self:
			del self[name]
		else:
			raise AttributeError('invalid attribute:\t%s' % name)

	def getObj(self):
		return ObjectDict(self)





# def load_json_file_as_obj(filename):
# 	data = None
# 	with open(filename, 'r') as f:
# 		data = json.load(f)

# 	return ObjectDict(data)