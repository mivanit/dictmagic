"""
flattening and unflattening hierarchies of dicts
lets you access `mydict['hello']['world']` with `mydict['hello/world']`
or vice versa

- `sep` : section separator (any char can be used)
	- ':' in the style of `configparser` from the standard library
	- '.' in the style of YAML
	- '/' in the style of unix, hdf5, and other things
"""

def flatten(in_dict : dict, sep : str = '/') -> dict:
	output = dict()

	for key,val in in_dict.items():
		if isinstance(val, dict):
			for dk,dv in flatten(val, sep).items():
				output[sep.join([key, dk])] = dv
		else:
			output[key] = val

	return output


def unflatten(in_dict, sep = '/') -> dict:
	output = dict()
	
	for key,val in in_dict.items():
		splitKey = key.split(sep, 1)
		if len(splitKey) == 1:
			# if first level
			output[splitKey[0]] = val
		else:
			# if deeper
			if splitKey[0] not in output:
				output[splitKey[0]] = dict()

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