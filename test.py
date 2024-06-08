# New class(has no base) class with the
# dynamic class initialization of type()
new = type('New', (object, ),
		dict(var1='GeeksforGeeks', b=2009))

print(new)
print(vars(new))


