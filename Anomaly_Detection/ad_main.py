
# configuration
import config_parser as configuration
import data_convert as dc
from datetime import datetime
import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates
import datetime as dt
import learn_utils
from sklearn.cluster import KMeans

##### required library #####
import pandas as pd

WINDOW_LEN = 60
def main():
    """
    Main function
    """
   

    print("Reading data...")
    data = dc.read_data('0002_00000039_voltage_0526_2.txt')

    dataset = pd.DataFrame(data, columns=['measure_time', 'voltage'])

    dataset['measure_time'] = pd.to_datetime(dataset['measure_time'], format='%Y-%m-%d %H:%M:%S.%f')
    dataset['voltage'] = dataset['voltage'].apply(pd.to_numeric, errors='ignore')
    
    dataset = dataset.set_index('measure_time')   

    data = dc.resample_missingValue(dataset, 100, 1)
    #data = data[data.voltage != 100]

    print(data)

    data = data['voltage'][500:1500]

    ########## windowing #########
    window_rads = np.linspace(0, np.pi, WINDOW_LEN)
    window = np.sin(window_rads)**2
    print("Windowing data...")
    windowed_segments = get_windowed_segments(data, window)
    print(windowed_segments)
    
    print("Produced %d waveform segments" % len(windowed_segments))

    from sklearn.cluster import KMeans

    clusterer = KMeans(n_clusters=150)

    # compute k-means clustering
    clusterer.fit(windowed_segments)


    import learn_utils

    learn_utils.plot_waves(clusterer.cluster_centers_, step=3)






'''
    #datelist = data[0:,0]
    

    # total datasize 72851
    # 101219 rows
    n_samples_to_plot = 1000
    plt.plot(data[0:n_samples_to_plot])
    
    plt.xlabel("timestamp")
    plt.ylabel("Voltage value")
    plt.show()

#    cfg = configuration.cfg_parser()
#    HOST = cfg.host
#    PORT = cfg.port
#    print(HOST)
'''

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




if __name__ == '__main__':
    main()