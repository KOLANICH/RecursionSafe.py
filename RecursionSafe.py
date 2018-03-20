from functools import wraps
class RecursionSafe:
	__slots__ = ("visiting",)
	
	class Lock:
		__slots__ = ("obj", "safe")
		def __init__(self, safe, obj):
			self.safe = safe
			self.obj = obj
		
		def __enter__(self):
			i = id(self.obj)
			if i not in self.safe.visiting:
				self.safe.visiting.add(i)
				return self.obj
			else:
				return ...
			
		def __exit__(self, *args, **kwargs):
			i = id(self.obj)
			if i in self.safe.visiting:
				self.safe.visiting.remove(i)
		
	def __init__(self):
		self.visiting = set()
	
	def __call__(self, obj):
		return self.__class__.Lock(self, obj)

	def wrap(self, f):
		@wraps(f)
		def wrapped(firstArg, *args, **kwargs):
			with self(firstArg) as firstArg:
				return f(firstArg, *args, **kwargs)
		return wrapped
