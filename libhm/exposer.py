from .util import *

def expcorr(img, level, func=np.mean):
    return ndarray_to_python(level / func(normalize(img), axis=(0, 1)))
def expcorr_max(img, level): return expcorr(img, level, np.max)
def expcorr_mean(img, level): return expcorr(img, level, np.mean)
def expcorr_perc(img, level, perc): return expcorr(img, level, lambda x, axis: np.percentile(x, perc, axis))