from __future__ import print_function
import ekg_data

ekg_filename = 'a02.dat'
ekg_data = ekg_data.read_ekg_data(ekg_filename)
print(ekg_data.shape)
ekg_data = ekg_data[0:8192]

print(ekg_data)
print(type(ekg_data))

"""
print("ekg_data[0]:\t", ekg_data[0])
print("ekg_data[1]:\t", ekg_data[1])
print("ekg_data.min:\t", ekg_data.min())
print("ekg_data.max:\t", ekg_data.max())

#%matplotlib inline

import matplotlib.pyplot as plt

n_samples_to_plot = 64
plt.plot(ekg_data[0:n_samples_to_plot])
plt.xlabel("Sample number")
plt.ylabel("Signal value")
plt.show()
"""
import numpy as np

segment_len = 32
slide_len = 2

segments = []
for start_pos in range(0, len(ekg_data), slide_len):
    end_pos = start_pos + segment_len
    # make a copy so changes to 'segments' doesn't modify the original ekg_data
    segment = np.copy(ekg_data[start_pos:end_pos])
    # if we're at the end and we've got a truncated segment, drop it
    if len(segment) != segment_len:
        continue
    segments.append(segment)

print("Produced %d waveform segments" % len(segments))

window_rads = np.linspace(0, np.pi, segment_len)
window = np.sin(window_rads)**2

windowed_segments = []
for segment in segments:
    windowed_segment = np.copy(segment) * window
    windowed_segments.append(windowed_segment)

print(windowed_segments)

import pdb; pdb.set_trace()  # breakpoint 5c4f529b //

# clustering by k-means algorithm

from sklearn.cluster import KMeans

clusterer = KMeans(n_clusters=150)

# compute k-means clustering
clusterer.fit(windowed_segments)


import learn_utils

learn_utils.plot_waves(clusterer.cluster_centers_, step=3)

