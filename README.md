# dictmagic
[`dictmagic`](https://github.com/mivanit/dictmagic) is a very small python 3 package that makes it easier to do certain weird things with dictionaries.  
At the moment, it lets you convert to and from "flattened" dictionaries that use path syntax instead of nested dictionaries, and simplifies the process of accessing python dictionary elements as attributes. This package is mostly written to loading, saving, using, and coverting between various configuration methods easier.

## installation
```
pip install dictmagic
```

# Usage
## `dictmagic.paths`
flattening and unflattening hierarchies of dicts lets you access `mydict['hello']['world']` with `mydict['hello/world']` or vice versa. This is useful in contexts where having nested dicts is not practical (hash maps that can be used in strictly typed languages, hdf5 attributes, etc)

- `dictmagic.paths.flatten()` or `dictmagic.flatten()`
- `dictmagic.paths.unflatten()` or `dictmagic.unflatten()`

### Arguments
(identical for both functions)
 - `in_dict` : input dictionary. not modified

- `sep` : section separator (any char can be used, `/` is default)
	- `/` in the style of unix, hdf5, and other things
	- `:` in the style of `configparser` from the standard library
	- `.` in the style of YAML

## `dictmagic.obj`
- `dictmagic.obj.ObjectDict` or `dictmagic.ObjectDict`

allows accessing elements of a dictionary as `object.key` instead of `object['key']`

why is this useful when you can just dump it into `object.__dict__` ?
primarily because doing that will make copying your dict rather difficult without ending up with somewhat of a mess.

# misc
originally developed by @mivanit for a config manager, then moved to [knc-tools](https://github.com/knc-neural-calculus/knc-tests) for a time. Check out that repo for more weird tools.

PRs and feature requests welcome!

## building
to build the package:
(you probably don't need to do this unless you're uploading a fork to PyPI)
```
python setup.py sdist bdist_wheel
```
