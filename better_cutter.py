import numpy as np
import math
from easygui import fileopenbox, filesavebox   # (assuming that’s how you opened files)
import pylab as pp

print("Choose your spectrum")
spectrum = np.loadtxt(fileopenbox(msg="Choose your spectrum"))

print("Choose your linelist")
linelist = np.loadtxt(fileopenbox(msg="Choose your linelist"))

linelist = sorted(linelist)
width = 0.3
padding = 0.02      # try a bit of extra padding so nothing leaks out

def Create_Mask(spectrum, linelist, width, padding=0.0):
    freqs = spectrum[:,0]
    N = freqs.shape[0]
    mask = np.ones(N, dtype=int)

    half_width = width / 2.0 + padding

    for line in linelist:
        low  = line - half_width
        high = line + half_width
        hit = (freqs >= low) & (freqs <= high)
        mask[hit] = 0

    return mask

# build the 0/1 mask
mask = Create_Mask(spectrum, linelist, width, padding)

# apply it to your intensity column
applymask = spectrum.copy()
applymask[:,1] *= mask

# save out
np.savetxt(filesavebox(msg="Save your Cut Spectrum"), applymask)
print("Idiot check: saved that shit successfully.")

# plot
pp.plot(applymask[:,0], applymask[:,1])
pp.xlabel("Frequency")
pp.ylabel("Intensity")
pp.show()
