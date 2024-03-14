from refvars import Reference

x = Reference[int](0)

x.set(3.14) # TypeError: Argument 1 of Reference.set is not of type int