import numpy as np
import math
from easygui import fileopenbox, filesavebox   # (assuming that’s how you opened files)
import pylab as pp

def read_linelist_file(fname):
    """Read a linelist file robustly and return 1D float array of line centers.
       If file has >1 column, take the first column."""
    try:
        data = np.loadtxt(fname)
    except Exception as e:
        print(f"Warning: could not read '{fname}': {e}")
        return np.array([], dtype=float)

    data = np.atleast_1d(data)
    if data.ndim == 1:
        return data.astype(float)
    else:
        # If multi-column, assume first column contains the line centers
        return data[:, 0].astype(float)

print("Choose your spectrum")
spectrum_path = fileopenbox(msg="Choose your spectrum")
if spectrum_path is None:
    raise SystemExit("No spectrum selected. Exiting.")
spectrum = np.loadtxt(spectrum_path)

print("Choose your linelist file(s) (you can pick multiple)")
linelist_paths = fileopenbox(msg="Choose your linelist(s)", multiple=True)

# handle the case where user picked a single file (easygui sometimes returns a string)
if linelist_paths is None:
    raise SystemExit("No linelist selected. Exiting.")
if isinstance(linelist_paths, str):
    linelist_paths = [linelist_paths]

# read all linelists and concatenate
all_lines = []
for p in linelist_paths:
    lines = read_linelist_file(p)
    if lines.size > 0:
        all_lines.append(lines)

if not all_lines:
    raise SystemExit("No valid linelist data found in selected files. Exiting.")

linelist = np.concatenate(all_lines)
linelist = np.unique(linelist)   # remove duplicates and sort
linelist = np.sort(linelist)

print(f"Combined {len(linelist_paths)} file(s) into {linelist.size} unique lines.")

# parameters
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
