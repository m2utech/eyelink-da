# -*- coding: utf-8-*-

import jpype
import jaydebeapi as jp
import pandas as pd
import pandas.io.sql as pd_sql
import matplotlib

# jdbc 파일 경로 및 class 경로 설정
JDBC_DRIVER = '../drivers/jdbc-4.2.9.jar'

# parstream 접근
conn = jp.connect('com.parstream.ParstreamDriver',
                  'jdbc:parstream://m2u-da.eastus.cloudapp.azure.com:9043/eyelink?user=parstream&password=Rornfldkf!2',
                  JDBC_DRIVER)


curs = conn.cursor()
sql = """
SELECT *
FROM tb_node_raw
WHERE event_time >= TIMESTAMP'2016-11-16 00:00:00' and event_time <= TIMESTAMP'2016-12-13 23:59:59' 
"""

curs.execute(sql)

#data = curs.fetchall()
data = pd.DataFrame(curs.fetchall())
print(data)

conn.close()

"""
SELECT 	node_id, CAST(event_type AS int32), 
		measure_time, event_time,
		CAST(voltage as double), CAST(ampere as double),
		CAST(power_factor as double), CAST(active_power as double),
		CAST(reactive_power as double), CAST(apparent_power as double),
		CAST(amount_active_power as double), CAST(als_level as int32),
		CAST(dimming_level as int32), CAST(vibration_x as int16),
		CAST(vibration_y as int16), CAST(vibration_z as int16),
		CAST(vibration_max as int16), CAST(noise_origin_decibel as int16),
		CAST(noise_origin_frequency as int16), CAST(noise_decibel as double),
		CAST(noise_frequency as int32), CAST(gps_longitude as double),
		CAST(gps_latitude as double), CAST(gps_altitude as double),
		CAST(gps_satellite_count as int16), CAST(status_als as int16),
		CAST(status_gps as int16), CAST(status_noise as int16),
		CAST(status_vibration as int16), CAST(status_power_meter as int16),
		CAST(status_emergency_led_active as int16), CAST(status_self_diagnostics_led_active as int16),
		CAST(status_active_mode as int16), CAST(status_led_on_off_type as int16),
		reboot_time, CAST(event_remain as int16), CAST(failfirmwareupdate as int32),
		event_year, event_month, event_day
"""