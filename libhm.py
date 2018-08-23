import ctypes as c
import numpy as np


def _normalize(arr):
    if arr.dtype.kind == 'f': return arr
    else: return arr / np.iinfo(arr.dtype).max


def _to_python(arr):
    return arr.tolist()


def pointer_to_ndarray(ptr, shape, dtype):
    ptr, shape, dtype = int(ptr), tuple(shape), str(dtype)
    cptr = c.c_void_p(ptr)
    ctype = np.ctypeslib._typecodes[np.dtype(dtype).str] # hack...
    return np.ctypeslib.as_array(c.cast(cptr, c.POINTER(ctype)), shape)

def print_array(img):
    if isinstance(img, np.ndarray):
        with open('c:/users/kosio/desktop/pythonlog.log', 'a') as out:
            print(img, file=out)

def expcorr(img, level, func=np.mean):
    return _to_python(level / func(_normalize(img), axis=(0, 1)))
def expcorr_max(img, level): return expcorr(img, level, np.max)
def expcorr_mean(img, level): return expcorr(img, level, np.mean)
def expcorr_perc(img, level, perc): return expcorr(img, level, lambda x, axis: np.percentile(x, perc, axis))


# img = np.ndarray((1024, 1280, 3), dtype=np.uint16)
# img[...] = np.arange(1280*3).reshape((-1, 3))
#
# arr = pointer_to_ndarray(img.__array_interface__['data'][0], img.shape, img.dtype.name)
