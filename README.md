# dictmagic
[`dictmagic`](https://github.com/mivanit/dictmagic) is a very small python 3 package that makes it easier to do certain weird things with dictionaries.  
At the moment, it lets you convert to and from "flattened" dictionaries that use path syntax instead of nested dictionaries, and simplifies the process of accessing python dictionary elements as attributes. This package is mostly written to loading, saving, using, and coverting between various configuration methods easier.

## installation
```
pip install dictmagic
```


## contents
[TOC]

# Usage
## using `dictmagic.paths`
flattening and unflattening hierarchies of dicts lets you access `mydict['hello']['world']` with `mydict['hello/world']` or vice versa. This is useful in contexts where having nested dicts is not practical (making hash maps that can be used in strictly typed languages, storing data in hdf5 attributes, etc)

- `dictmagic.paths.flatten()` or `dictmagic.flatten()`
- `dictmagic.paths.unflatten()` or `dictmagic.unflatten()`

### Overview
(identical for both functions)
 - `in_dict` : input dictionary. not modified

- `sep` : section separator (any char can be used, `/` is default)
	- `/` in the style of unix, hdf5, and other things
	- `:` in the style of `configparser` from the standard library
	- `.` in the style of YAML


### using `paths.flatten()`
 - Args:
   - `in_dict` (dict): input (nested) dictionary
   - `sep` (str, optional): separator between nested dicts. Defaults to '/'.
   - `except_nonstr_key` (bool, optional): if True, raise exception if non-string key found. If False, converts key to string and proceeds. Defaults to True.

 - Returns:
   - `dict`: flattened dictionary

 - Raises:
   - `TypeError`: if non-string key found (including in dup_key_repl)


### using `paths.unflatten()`
 - Args:
   - `in_dict` ([type]): unput dictionary
   - `sep` (str, optional): separator between nested paths in `in_dict`. Defaults to '/'.
   - `except_dup_key` (bool, optional): if True, raise exception if a duplicate key is found. For behavior if False, see below. Defaults to True.
   - `dup_key_repl` ([type], optional): if exception is not raised, map duplicate to this value:
  	if `D` contains
  		`{ 'a' : 'val1', 'a/b' : 'val2' }`
  	then `unflatten(D)` will have
  		`{ 'a' : { dup_key_repl : 'val1', 'b' : 'val2' } }`
  	Defaults to None.
   - `except_nonstr_key` (bool, optional): if True, raise exception if non-string key found. If False, converts key to string and proceeds. Defaults to True.

 - Raises:
   - `KeyError`: if `except_dup_key` is True, raises key error when duplicate key found
   - `TypeError`: if non-string key found (including in `dup_key_repl`)

 - Returns:
   - `dict`: nested dictionary



## using `dictmagic.obj`
- `dictmagic.obj.ObjectDict` or `dictmagic.ObjectDict`

this class, taking a single argument `data`, allows accessing elements of a that dictionary as `object.key` instead of `object['key']`.

why is this useful when you can just dump it into `object.__dict__` ?
primarily because doing that will make copying your dict rather difficult without ending up with somewhat of a mess.

# misc
originally developed by @mivanit for a config manager, then moved to [knc-tools](https://github.com/knc-neural-calculus/knc-tests) for a time. Check out that repo for more weird tools.

PRs and feature requests welcome!

you can find this project on PyPI: [pypi.org/project/dictmagic/](https://pypi.org/project/dictmagic/)

## building
to build the package:
(you probably don't need to do this unless you're uploading a fork to PyPI)
```
python setup.py sdist bdist_wheel
```
