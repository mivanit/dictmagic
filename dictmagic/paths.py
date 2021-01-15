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
