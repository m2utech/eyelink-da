import pandas as pd

ap_assignments = {0: [], 1: ['0002.00000025', '0002.0000003F', '0001.00000001', '0002.00000039', '0001.00000018'], 2: ['0001.00000016', '0001.0000001C', '0002.00000024', '0001.00000002', '0001.0000001A', '0002.00000023', '0001.00000011', '0001.0000000C', '0002.0000002E', '0001.00000007', '0002.00000038', '0001.00000045', '0001.0000003A', '0002.0000002A', '0002.00000036', '0001.00000015', '0001.00000009', '0001.00000006', '0002.0000003E', '0002.00000033', '0002.0000002D', '0002.00000034', '0001.00000043', '0002.00000020', '0001.00000014', '0002.00000035', '0001.00000013', '0001.0000000B', '0002.00000028', '0002.00000037', '0001.0000000E', '0002.00000027', '0001.00000012', '0001.0000001E', '0001.00000004', '0001.00000017'], 3: ['0001.0000002F', '0001.00000019', '0002.0000002C', '0002.00000026', '0001.00000005', '0001.0000001D', '0001.0000003B', '0001.00000044', '0001.00000030', '0001.00000031', '0002.0000001F']}

ap_assign = ",".join(map(str, list(ap_assignments.values())))
print("test==== {}".format(ap_assign))
ap_assign = ap_assign.replace(", ",":").replace("'","").replace("[","").replace("]","")
ap_assign = ap_assign.split(',')
print(ap_assign)
ap_assign = pd.DataFrame(ap_assign).T

import pdb; pdb.set_trace()  # breakpoint feadf142 //

from datetime import date
from dateutil.relativedelta import relativedelta
import time


year2 = 2016

print(type(str(year2)[:3]))

import pdb; pdb.set_trace()  # breakpoint c3892a76 //


s1 = [0.99332, 0.9931485, 0.9924255, 0.9, 0.983919, 0.9849565, 0.9927825, 0.992611, 0.9929680000000001, 0.992954, 0.9924165, 0.9924255, 0.9845615, 0.9844615, 0.976245, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.989828, 0.9808945, 0.98939, 0.9798215, 0.989394, 0.9701139999999999, 0.9798910000000001, 0.9799709999999999, 0.970464, 0.988726, 0.98939, 0.970464]
s2 = [0.9711835, 0.989828, 0.990252, 0.9, 0.9812435, 0.981306, 0.980541, 0.980391, 0.9906635, 0.9810315000000001, 0.981306, 0.9722310000000001, 0.99046, 0.9812435, 0.9715370000000001, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.99224, 0.9814515, 0.9828749999999999, 0.9823405000000001, 0.9910699999999999, 0.9811025, 0.9812435, 0.9812435, 0.9718775, 0.989823, 0.970472, 0.9808945]
r = 5

for ind, i in enumerate(s1):

        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        print((ind-r if ind-r >= 0 else 0))
        print("=========")
        print(ind, i, lower_bound, upper_bound)


#    return float(np.sqrt(LB_sum))

import pdb; pdb.set_trace()  # breakpoint 2ae94c21 //



#from datetime import datetime, timedelta

#start = time.perf_counter()
start = time.time()
now = time.asctime()

print(type(start))
print(now)

print("test : {}, now : {}".format(start,now))
print("running time:")
end = time.time()
print("============")
#print("running time: %.03f" % (end - start))
print("running time: {0:.03f}".format(end - start))
print(end-start)


################## 1 day ##################
today = date.today()
#minusDay = timedelta(days=121)
minusDay = relativedelta(days=121)
startDate = today - minusDay
endDate = startDate


test = '{"start_date":"'+ startDate.strftime('%Y-%m-%d') + '", "end_date":"' + endDate.strftime('%Y-%m-%d') + '", "time_interval": 15}'
test = test.encode()

print(test)
print(type(test))

################## 1 week ##################
today = date.today()
minusDay = relativedelta(days=121)
oneWeek = relativedelta(days=6)
endDate = today - minusDay
startDate = endDate - oneWeek


test = '{"start_date":"'+ startDate.strftime('%Y-%m-%d') + '", "end_date":"' + endDate.strftime('%Y-%m-%d') + '", "time_interval": 15}'
test = test.encode()

print(test)
print(type(test))

################## 1 month ##################
today = date.today()
premonth = today - relativedelta(months=5)
startDate = date(premonth.year, premonth.month, 1)
endDate = date(today.year, today.month, 1) - relativedelta(months=4) - relativedelta(days=1)


test = '{"start_date":"'+ startDate.strftime('%Y-%m-%d') + '", "end_date":"' + endDate.strftime('%Y-%m-%d') + '", "time_interval": 15}'
test = test.encode()

print(test)
print(type(test))
