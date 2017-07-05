import json
import time
import numpy as np
import data_convert
import learn_utils
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

WINDOW_LEN = 30

def main(node_id, s_date, e_date, t_interval):
    # running time check
    #start_time = time.time()
    #logger.info("Dataset Loading...")
    print("condition check..........")
    # json data load
    dataset = data_convert.json_data_load(node_id, s_date, e_date)
    #print(dataset)
    #plt.plot(dataset)
    #plt.show()

    #dataset = dataset.resample('1T').mean()
    #dataset = dataset.fillna(220)
    #dataset = dataset.reset_index()
    #dataset = dataset.voltage
    #dataset = dataset[dataset.notnull()]
    
    #print(dataset)
    #dataset = dataset[dataset.voltage != -999]
    #dataset = dataset[dataset.voltage.notnull()]
    #plt.plot(dataset)
    #plt.show()


    ##################
    # data resampling
    # (dataset, default value, time interval)
    dataset = data_convert.resample_missingValue(dataset, 220, 1)
    

    # 추후 속성별 데이터 로드 
    attr = 'voltage'  
    data = data_convert.extract_attribute(dataset, attr)
    #print(data)
    #print(type(data))

#    dataset = pd.DataFrame(data)
#    print(dataset)
#    dataset.voltage += 100
#    print(dataset)
    #########-100 ##########
    #data -= 100
    #print("========")
    #print(data)

    # sliding_chunker(data, window_len, slide_len)
    # not apply sine signal
    print("extracting segment...")
    segments = learn_utils.sliding_chunker(data,WINDOW_LEN,5)
    print("Produced %d waveform segments" % len(segments))
    ##learn_utils.plot_waves(segments, 5, 6, 6)


    ##############################
    ########## windowing #########
    window_rads = np.linspace(0, np.pi, WINDOW_LEN)
    window = np.sin(window_rads)**2
    #plt.plot(window)
    #plt.show()

    print("Windowing data...")
    windowed_segments = get_windowed_segments(data, window)
    print("Produced %d waveform windowed segments" % len(windowed_segments))
    ##learn_utils.plot_waves(windowed_segments, 5, 6, 6)

    ########################################
    ## clustering using K-Means algorithm ##
    ########################################
    print("Clustering data...")
    clusterer = KMeans(n_clusters=30)
    #clusterer = KMeans()
    # compute k-means clustering
    clusterer.fit(windowed_segments)
    print(clusterer.cluster_centers_)
    #plt.plot(clusterer.cluster_centers_)
    #plt.show()
    learn_utils.plot_waves(clusterer.cluster_centers_, 1, 5, 6)


    print("Reconstructing...")
    reconstruction = learn_utils.reconstruct(data, window, clusterer)
    error = reconstruction - data

    print("Maximum reconstruction error is %.1f" % max(error))
    #learn_utils.plot_waves(reconstruction, 1, 4, 4)
    plt.figure()
    #plt.plot(data[0:10000], label="Original voltage")
    plt.plot(data, label="Original voltage")
    #plt.legend()
    #plt.show()
    plt.plot(reconstruction, label="Reconstructed voltage")
    #plt.legend()
    #plt.show()

    plt.plot(error, label="Reconstruction Error")
    plt.legend()
    plt.show()
    print(error)

    import pdb; pdb.set_trace()  # breakpoint a3ed6eb3 //


    learn_utils.plot_waves(clusterer.cluster_centers_, step=15)


def get_windowed_segments(data, window):
    step = 5
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
	import socket_client_test
    #pass