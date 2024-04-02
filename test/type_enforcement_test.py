from refvars import Make_Reference

x = Make_Reference[int](0).reference

# NOTE: The below should raise a TypeError.
# NOTE:  This is intended behavior, hence the `#type:ignore` comment.
x.set(3.14) #type:ignore
