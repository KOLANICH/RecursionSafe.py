RecursionSafe.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![PyPi Status](https://img.shields.io/pypi/v/RecursionSafe.py.svg)](https://pypi.python.org/pypi/RecursionSafe.py)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/RecursionSafe.py.svg?branch=master)](https://travis-ci.org/KOLANICH/RecursionSafe.py)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/RecursionSafe.py.svg)](https://coveralls.io/r/KOLANICH/RecursionSafe.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/RecursionSafe.py.svg)](https://libraries.io/github/KOLANICH/RecursionSafe.py)

A context manager to protect you from infinite recursion when walking collections.

Just wrap a recursive function with it. If you visit any object you are already in you will get ellipsis instead of the object, be ready for it.

Example
-------
```python
recSafe=RecursionSafe()

objs={
	'a':{},
	'a.b':{},
	'a.b.c': {},
	'a.b.d': {},
	'a.b.c.d': 14,
	'a.e': 10,
	'a.f':{},
}

objs['a']["b"]=objs['a.b']
objs['a.b']["c"]=objs['a']
objs['a.b']["d"]=objs['a.b.d']
objs['a.b.c']["d"]=objs['a.b.c.d']
objs['a']["e"]=objs['a.e']
objs['a']["f"]=objs['a.f']
objs['a.f']["g"]=objs['a']
a=objs['a']

idsToNames={id(objs[k]):k for k in objs}

@recSafe.wrap
def ownRepr(a):
	if isinstance(a, dict):
		return "{"+", ".join((ownRepr(k)+":"+ownRepr(v) for k, v in a.items()))+"}"
	else:
		return repr(a)
print("repr", repr(a)) # even non-recursive objects are ellipsed
print("ownRepr", ownRepr(a))  # feel the difference - non-self-referencing objects are not ellipsed
```

Requirements
------------
* [```Python 3```](https://www.python.org/downloads/). ```Python 2``` is dead, stop raping its corpse. Use ```2to3``` with manual postprocessing to migrate incompatible code to ```3```. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their ```dict``` is ordered and deterministic.