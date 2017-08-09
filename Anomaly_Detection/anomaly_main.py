import json
import time
import numpy as np
import data_convert
import learn_utils
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#for test
node_id = '0002.00000039'
s_date = '2017-01-01'
e_date = '2017-01-31'
WINDOW_LEN = 60

def main(node_id, s_date, e_date, t_interval):
    # running time check
    #start_time = time.time()
    #logger.info("Dataset Loading...")
    print("condition check..........")
    # json data load
    
    dataset = data_convert.json_data_load(node_id, s_date, e_date)
    # dataset.describe()
    # dataset.info()
    #sns.pairplot(dataset)
    #plt.show()


    ##################
    # process of data missing value and resampling
    # resample_missingValue(data, default_value, t_interval)
    voltage_data = data_convert.resample_missingValue(dataset['voltage'], 220, 1)
    ampere_data = data_convert.resample_missingValue(dataset['ampere'], 0.5, 1)
    active_power_data = data_convert.resample_missingValue(dataset['active_power'], 110, 1)
    power_factor_data = data_convert.resample_missingValue(dataset['power_factor'], 0.9, 1)
    
    # 각 데이터 하나로 merge
    mergedata = pd.concat([voltage_data, ampere_data.ampere, active_power_data.active_power, power_factor_data.power_factor], axis=1, join_axes=[voltage_data.index])   
    #print(voltage_data.sample(10))
    #print(ampere_data.sample(10))
    #print(mergedata = dataset.iloc[:,:])

    plt.figure(figsize=(20,18))
    ax1 = plt.subplot(4,1,1)
    plt.plot(mergedata.index, mergedata.voltage, c='r')
    plt.ylabel("Voltage")

    ax2 = plt.subplot(4,1,2)
    plt.plot(mergedata.index, mergedata.ampere, c='b')
    plt.ylabel("Ampere")

    ax3 = plt.subplot(4,1,3)
    plt.plot(mergedata.index, mergedata.active_power, c='g')
    plt.ylabel("Active Power")

    ax4 = plt.subplot(4,1,4)
    plt.plot(mergedata.index, mergedata.power_factor, c='m')
    plt.ylabel("Power Factor")

    plt.show()

    import pdb; pdb.set_trace()  # breakpoint f8ca90ee //

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
    #learn_utils.plot_waves(segments, 60, 6, 20)


    ##############################
    ########## windowing #########
    #window_rads = np.linspace(0, np.pi, WINDOW_LEN)

    print("Windowing data...")
    #window_rads = np.linspace(0, 3.7, WINDOW_LEN)
    #window = np.sin(window_rads)**2
    #windowed_segments = learn_utils.get_windowed_segments(data, window)
    #print("Produced %d waveform windowed segments" % len(windowed_segments))
    #earn_utils.plot_waves(windowed_segments, 60, 6, 20)

    ########################################
    ## clustering using K-Means algorithm ##
    ########################################
    print("Clustering data...")
    clusterer = KMeans(n_clusters=100)
    #clusterer = KMeans()
    # compute k-means clustering
    
    #clusterer.fit(windowed_segments)
    clusterer.fit(segments)

    #print(clusterer.cluster_centers_)
    #plt.plot(clusterer.cluster_centers_)
    #plt.show()
    learn_utils.plot_waves(clusterer.cluster_centers_, 1, 5, 20)


    print("Reconstructing...")
    reconstruction = learn_utils.reconstruct(data, 60, clusterer)
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

    import pdb; pdb.set_trace()  # breakpoint f9c4fcdc //


    learn_utils.plot_waves(clusterer.cluster_centers_, step=15)


	#running_time = time.time() - start_time
	#logger.info("Start-date:{0} | End-date:{1} | Time-interval:{2} >> Running-time:{3:.03f} sec".format(start_date,end_date,time_interval, running_time))

if __name__ == '__main__':
	# import socket_client_test
    main("0002.00000039", '2016-12-01', '2017-01-31', 15)
    #pass