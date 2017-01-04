# -*- coding: utf-8-*-

import pandas as pd
#import numpy as np


def read_file():
	# csv or text 파일, 구분자','
	dataset = pd.read_csv("../data/busan_tb_node_raw_1215_test.txt", sep=',', parse_dates=[2,3])
	
	# 파스트림 연동시를 위해 소문자로..
	dataset.rename(columns = {'NODE_ID' : 'node_id'}, inplace = True)
	dataset.rename(columns = {'EVENT_TYPE' : 'event_type'}, inplace = True)
	dataset.rename(columns = {'MEASURE_TIME' : 'measure_time'}, inplace = True)
	dataset.rename(columns = {'EVENT_TIME' : 'event_time'}, inplace = True)
	dataset.rename(columns = {'VOLTAGE' : 'voltage'}, inplace = True)
	dataset.rename(columns = {'AMPERE' : 'ampere'}, inplace = True)
	dataset.rename(columns = {'POWER_FACTOR' : 'power_factor'}, inplace = True)
	dataset.rename(columns = {'ACTIVE_POWER' : 'active_power'}, inplace = True)
	dataset.rename(columns = {'REACTIVE_POWER' : 'reactive_power'}, inplace = True)
	dataset.rename(columns = {'APPARENT_POWER' : 'apparent_power'}, inplace = True)
	dataset.rename(columns = {'AMOUNT_OF_ACTIVE_POWER' : 'amount_of_active_power'}, inplace = True)

	# 모든 속성 이용시..
	dataset.rename(columns = {'ALS_LEVEL' : 'als_level'}, inplace = True)
	dataset.rename(columns = {'DIMMING_LEVEL' : 'dimming_level'}, inplace = True)
	dataset.rename(columns = {'VIBRATION_X' : 'vibration_x'}, inplace = True)
	dataset.rename(columns = {'VIBRATION_Y' : 'vibration_y'}, inplace = True)
	dataset.rename(columns = {'VIBRATION_Z' : 'vibration_z'}, inplace = True)
	dataset.rename(columns = {'VIBRATION_MAX' : 'vibration_max'}, inplace = True)
	dataset.rename(columns = {'NOISE_ORIGIN_DECIBEL' : 'noise_origin_decibel'}, inplace = True)
	dataset.rename(columns = {'NOISE_ORIGIN_FREQUENCY' : 'noise_orgin_frequency'}, inplace = True)
	dataset.rename(columns = {'NOISE_DECIBEL' : 'nosie_decibel'}, inplace = True)
	dataset.rename(columns = {'NOISE_FREQUENCY' : 'noise_frequency'}, inplace = True)
	dataset.rename(columns = {'GPS_LONGITUDE' : 'gps_longtude'}, inplace = True)
	dataset.rename(columns = {'GPS_LATITUDE' : 'gpsi_latitude'}, inplace = True)
	dataset.rename(columns = {'GPS_ALTITUDE' : 'gps_altitude'}, inplace = True)
	dataset.rename(columns = {'GPS_SATELLITE_COUNT' : 'gps_stellite_count'}, inplace = True)
	dataset.rename(columns = {'STATUS_ALS' : 'status_als'}, inplace = True)
	dataset.rename(columns = {'STATUS_GPS' : 'status_gps'}, inplace = True)
	dataset.rename(columns = {'STATUS_NOISE' : 'status_noise'}, inplace = True)
	dataset.rename(columns = {'STATUS_VIBRATION' : 'status_vibration'}, inplace = True)
	dataset.rename(columns = {'STATUS_POWER_METER' : 'status_power_meter'}, inplace = True)
	dataset.rename(columns = {'STATUS_EMERGENCY_LED_ACTIVE' : 'status_fmergency_led_active'}, inplace = True)
	dataset.rename(columns = {'STATUS_SELF_DIAGNOSTICS_LED_ACTIVE' : 'status_self_diagnostics_led_active'}, inplace = True)
	dataset.rename(columns = {'STATUS_ACTIVE_MODE' : 'status_active_mode'}, inplace = True)
	dataset.rename(columns = {'STATUS_LED_ON_OFF_TYPE' : 'status_led_on_off_type'}, inplace = True)
	dataset.rename(columns = {'REBOOT_TIME' : 'reboot_time'}, inplace = True)
	dataset.rename(columns = {'EVENT_REMAIN' : 'event_remain'}, inplace = True)
	dataset.rename(columns = {'FAILFIRMWAREUPDATE' : 'failfirmwareupdate'}, inplace = True)


	dataset.reboot_time = pd.to_datetime(dataset.reboot_time)
	#dataset.index = dataset.event_time

	myJSON = dataset.reset_index().to_json("C:\\test.json", orient='records')

	return dataset


read_file()
"""
# 데이터 타입 정의 
# (DtypeWarning: Columns (xx) have mixed types.  방지
	dataset.event_type = dataset.event_type.astype(np.int8)
	dataset.voltage = dataset.voltage.astype(np.float32)
	dataset.ampere = dataset.ampere.astype(np.float32)
	dataset.power_factor = dataset.power_factor.astype(np.float32)
	dataset.active_power = dataset.active_power.astype(np.float32)
	dataset.reactive_power = dataset.reactive_power.astype(np.float32)
	dataset.apparent_power = dataset.apparent_power.astype(np.float32)
	dataset.amount_of_active_power = dataset.amount_of_active_power.astype(np.float32)
	dataset.als_level = dataset.als_level.astype(np.float32)
	dataset.dimming_level = dataset.dimming_level.astype(np.float32)
	dataset.vibration_x = dataset.vibration_x.astype(np.float32)
	dataset.vibration_y = dataset.vibration_y.astype(np.float32)
	dataset.vibration_z = dataset.vibration_z.astype(np.float32)
	dataset.vibration_max = dataset.vibration_max.astype(np.float32)
"""