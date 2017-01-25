testJson = {'tb_da_clustering_master': '[["2017-01-25T10:08:59Z","2016-12-08","2016-12-08",15,"0002.00000036:0002.00000033:0002.0000002A:0002.00000037:0002.00000038:0002.00000039:0002.0000003E:0002.00000028:0001.00000015:0002.00000029:0002.0000002C:0002.0000002D:0002.0000003F:0002.0000001F:0002.00000020:0002.0000002E:0001.00000014:0002.00000022","","",""]]'}

print(testJson)
print(type(testJson))

testJson = testJson.replace("'[","").replace("]'","")
print('+===============+')
print(testJson)
print(type(testJson))

import pdb; pdb.set_trace()  # breakpoint 63fdb8f3 //

testJson.collegeId = {"eventno": "6062","eventdesc": "abc"};
print('+===============+')
print(testJson)
print(type(testJson))
