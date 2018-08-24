import ctypes as c
import numpy as np

def normalize(arr):
    if arr.dtype.kind == 'f': return arr
    else: return arr / np.iinfo(arr.dtype).max

def ndarray_to_python(arr):
    return arr.tolist()

def pointer_to_ndarray(ptr, shape, dtype):
    ptr, shape, dtype = int(ptr), tuple(shape), str(dtype)
    cptr = c.c_void_p(ptr)
    ctype = np.ctypeslib._typecodes[np.dtype(dtype).str] # hack...
    return np.ctypeslib.as_array(c.cast(cptr, c.POINTER(ctype)), shape)