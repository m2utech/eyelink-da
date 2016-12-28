import numpy as np;
import seaborn as sns;
import pandas as pd
from scipy import stats
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt

num_samples = 61
group_size = 10

x = np.linspace(0, 15, num_samples)
a = np.sin(x) + np.linspace(0, 5, num_samples)

x = np.linspace(0, 50, num_samples)
b = np.sin(x) + np.linspace(0, -8, num_samples)
c = np.sin(x + 2)

d = np.linspace(0, 14, num_samples)
e = np.random.randn(group_size, 1) + np.linspace(0, -3, num_samples)

x = np.linspace(0, 4, num_samples)
f = np.sin(x)

timeSeries = pd.DataFrame()
ax = None
for arr in [a,b,c,d,e,f]:
    arr = arr + np.random.rand(group_size, num_samples) + (np.random.randn(group_size, 1)*3)
    df = pd.DataFrame(arr)
    timeSeries = timeSeries.append(df)

    # We use seaborn to plot what we have
    #ax = sns.tsplot(ax=ax, data=df.values, ci=[68, 95])
    ax = sns.tsplot(ax=ax, data=df.values, err_style="unit_traces")
plt.show(ax)
