import json
import time
import numpy as np
import data_convert
import learn_utils
from sklearn.cluster import KMeans

WINDOW_LEN = 60

def main(node_id, s_date, e_date, t_interval):

	# running time check
	start_time = time.time()
	#logger.info("Dataset Loading...")
	print("option check..........")

	# json data load
	dataset = data_convert.json_data_load(node_id, s_date, e_date)
	print(dataset)
	# data resampling
	dataset = data_convert.resample_missingValue(dataset, 100, 1)
	print(dataset)
	import pdb; pdb.set_trace()  # breakpoint 3c680ce6 //

	data = dataset['voltage']

	########## windowing #########
	window_rads = np.linspace(0, np.pi, WINDOW_LEN)
	window = np.sin(window_rads)**2
	print("Windowing data...")
	windowed_segments = get_windowed_segments(data, window)
	#print(windowed_segments)

	print("Produced %d waveform segments" % len(windowed_segments))

	from sklearn.cluster import KMeans

	clusterer = KMeans(n_clusters=60)
	#clusterer = KMeans()
	# compute k-means clustering
	clusterer.fit(windowed_segments)

	print(clusterer.cluster_centers_)


	import pdb; pdb.set_trace()  # breakpoint eefc1a67 //
# reconstruction
    print("Reconstructing...")
    reconstruction = learn_utils.reconstruct(data, window, clusterer)
    error = reconstruction - data
    print("Maximum reconstruction error is %.1f" % max(error))


	import learn_utils

	learn_utils.plot_waves(clusterer.cluster_centers_, step=15)


def get_windowed_segments(data, window):
    step = 2
    windowed_segments = []
    segments = learn_utils.sliding_chunker(
        data,
        window_len=len(window),
        slide_len=step
    )
    for segment in segments:
        segment *= window
        windowed_segments.append(segment)
    return windowed_segments


	#running_time = time.time() - start_time
	#logger.info("Start-date:{0} | End-date:{1} | Time-interval:{2} >> Running-time:{3:.03f} sec".format(start_date,end_date,time_interval, running_time))

if __name__ == '__main__':
	pass