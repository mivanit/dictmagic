"""
flattening and unflattening hierarchies of dicts
lets you access `mydict['hello']['world']` with `mydict['hello/world']`
or vice versa

- `sep` : section separator (any char can be used)
	- ':' in the style of `configparser` from the standard library
	- '.' in the style of YAML
	- '/' in the style of unix, hdf5, and other things
"""

def flatten(
		in_dict : dict,
		sep : str = '/',
		except_nonstr_key = True,
	) -> dict:
	"""flatten a dictionary

	takes dictionary with structure
		mydict['hello']['world']
	and maps that to a flattened dict:
		mydict['hello/world']

	Args:
		in_dict (dict): input (nested) dictionary
		sep (str, optional): separator between nested dicts. Defaults to '/'.
		except_nonstr_key (bool, optional): if True, raise exception if non-string key found. If False, converts key to string and proceeds. Defaults to True.

	Returns:
		dict: flattened dictionary

	Raises:
		TypeError: if non-string key found (including in dup_key_repl)
	"""
	output = dict()

	for key,val in in_dict.items():
		if not isinstance(key, str):
			if except_nonstr_key:
				raise TypeError('non-string key')
			else:
				key = str(key)

		if isinstance(val, dict):
			for dk,dv in flatten(val, sep).items():
				output[sep.join([key, dk])] = dv
		else:
			output[key] = val

	return output


def unflatten(
		in_dict,
		sep = '/',
		except_dup_key = True,
		dup_key_repl = None,
		except_nonstr_key = True,
	) -> dict:
	"""unflatten a nested dictionary

	Args:
		in_dict ([type]): unput dictionary
		sep (str, optional): separator between nested paths in `in_dict`. Defaults to '/'.
		except_dup_key (bool, optional): if True, raise exception if a duplicate key is found. For behavior if False, see below. Defaults to True.
		dup_key_repl ([type], optional): if exception is not raised, map duplicate to this value:
				if `D` contains
					{ 'a' : 'val1', 'a/b' : 'val2' }
				then `unflatten(D)` will have
					{ 'a' : { dup_key_repl : 'val1', 'b' : 'val2' } }
			Defaults to None.
		except_nonstr_key (bool, optional): if True, raise exception if non-string key found. If False, converts key to string and proceeds. Defaults to True.

	Raises:
		KeyError: if except_dup_key is True, raises key error when duplicate key found
		TypeError: if non-string key found (including in dup_key_repl)

	Returns:
		dict: nested dictionary
	"""
	output = dict()
	
	for key,val in in_dict.items():
		if not isinstance(key, str):
			if except_nonstr_key:
				raise TypeError('non-string key')
			else:
				key = str(key)
		
		splitKey = key.split(sep, 1)
		if len(splitKey) == 1:
			# if first level
			if splitKey[0] in output:
				if except_dup_key:
					raise KeyError('duplicate key')
				output[splitKey[0]].update({dup_key_repl : val})
			else:
				output[splitKey[0]] = val
		else:
			# if deeper
			if splitKey[0] not in output:
				output[splitKey[0]] = dict()
			
			if not isinstance(output[splitKey[0]], dict):
				if except_dup_key:
					raise KeyError('duplicate key')
				# if the key already maps to something other than a dict
				# make it map to a dict
				oldval = output[splitKey[0]]
				output[splitKey[0]] = { dup_key_repl : oldval }

			# map to val
			output[splitKey[0]][splitKey[1]] = val

	# do subsequent layers
	for k,v in output.items():
		if isinstance(v, dict):
			output[k] = unflatten(v, sep)

	return output



'''

# TODO: this is old code, might be useful for when a single (large) object needs to be viewed as both a flattened and unflattened dict. not currently working.

class HierarchyDict(dict):
	
	def __init__(self, in_dict, mode = 'm', sep='/'):
		"""
		flattening and unflattening hierarchies of dicts
		lets you access `mydict['hello']['world']` with `mydict['hello/world']`
		load the dict using `load_stdDict()` or `load_hDict`

		Args:
		- `in_dict` : input dictionary
		- `mode` : format of input dictionary:
		  - 's' for standard/nested
		  - 'f' for flattened
		  - 'm' for mixed/auto
		
		- `sep` : section separator (any char can be used)
		  - ':' in the style of `configparser` from the standard library
		  - '.' in the style of YAML
		  - '/' in the style of unix, hdf5, and other things
		"""

		self.sep = sep

		if mode == 's':
			self.load_stdDict(in_dict)
		elif mode == 'f':
			self.load_fDict(in_dict, sep = sep)
		elif mode == 'm':
			self.load_mixDict(in_dict, sep = sep)

	def load_stdDict(self, in_dict):
		self = copy.deepcopy(in_dict)

	def as_stdDict(self):
		return copy.deepcopy(dict(self))

	def as_hDict(self, sep : str = None):
		"""
		return a flattened dict with separator `sep`
		if `sep` is none, use the default specified during class creation
		"""
		if sep is None:
			sep = self.sep
			
		output = dict()
		

	@classmethod
	def load_fDict(cls, in_dict : dict, sep : str = '/') -> HierarchyDict:
		"""
		read a fully flattened dict with separator `sep`
		"""

		output = dict()

		for key,val in in_dict.items():
			splitKey = key.split(sep, 1)
			if len(splitKey) == 1:
				self[key] = val
			else:
				self[splitKey[0]] = splitKey[1]

	@classmethod
	def load_mixDict(self, in_dict, sep = None):
		"""
		read a mixed nested/flattened dict with separator `sep`
		if `sep` is none, use the default specified during class creation
		"""
		if sep is None:
			sep = self.sep

		for key,val in in_dict.items():
			splitKey = key.split(self.sep, 1)
			if len(splitKey) > 1:
				self[splitKey[0]] = 1
			else:
				self[key] = val

	@staticmethod
	def merge_nested_dicts(A, B):
		"""
		`A` will be modified, `B` will not
		behavior:
		- if `A[x]` exists, but B[x] does not, A[x] is unchanged
		- if `A[x]` does not exist, but `B[x]` does, `A[x] = deepcopy(B[x])`
		- if `A[x]` exists and has valid keys `{h,i,j}`, and `B[x]` exists and has valid keys `{i,j,k}` then recurse:
		- `A[x][h]` is unchanged
		- `A[x][i], A[x][j] = B[x][i], B[x][j]` 
		- `A[x][k] = B[x][k]`
		Returns:
		`None`, because A is modified
		"""
		# do nothing if key not in B
		for key,val in B.items():
			# write new if key not in A
			if key not in A:
				A[key] = val
			else:
				if type(A[key]) is dict:
					HierarchyDict.merge_nested_dicts(A[key], B[key])
				else:
					# overwrite if not a dict
					A[key] = B[key]
'''