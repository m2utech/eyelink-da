import unittest
import json
import pandas as pd
from anomaly_main import json_parsing
from data_convert import json_data_load
import data_convert as dc

class AnomalyDetectionTestCase(unittest.TestCase):

	def test_json_parsing(self):
		data = b'{"node_id": "0002.00000039", "start_date": "2016-12-01", "end_date": "2017-02-09", "time_interval": 15}'
		dict = json.loads(data.decode("utf-8")) # dictionary type
		node_id = dict['node_id']
		s_date = dict['start_date']
		e_date = dict['end_date']
		t_interval = dict['time_interval']

		self.assertEqual(node_id, "0002.00000039")
		self.assertEqual(s_date, "2016-12-01")
		self.assertEqual(e_date, "2017-02-09")
		self.assertEqual(t_interval, 15)

	def test_json_data_load(self):
		# check empty dataset
		dataset = json_data_load("0002.00000039","2016-12-01","2017-02-09")
		self.assertFalse(dataset.empty)

	def test_data_resample_missingValue(self):
		event_time = pd.date_range('12/1/2016', periods=9, freq='T')
		series = pd.Series(range(9), index=event_time)
		dataset = dc.resample_missingValue(series,100,1)
		self.assertFalse(dataset.empty)


unittest.main()