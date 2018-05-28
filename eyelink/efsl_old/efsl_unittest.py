import unittest
import ca_clustering as CA
import ad_matching as PM

sDate = "2018-01-15T00:00:00Z"
eDate = "2018-01-16T00:00:00Z"
testIndex = 'corecode'
testType = 'corecode'
tInterval = 10

class caClusteringTest(unittest.TestCase):
    def test_getDateRange(self):
    	result = CA.getDateRange(sDate, eDate, tInterval)
    	print(result)
        # self.assertIsNotNone(CA.getDateRange(sDate, eDate, tInterval))

    def test_getDataset(self):
    	result = CA.getDataset(sDate, eDate, testIndex, testType)
    	print(result)
        # self.assertIsNotNone(CA.getDataset(sDate, eDate, testIndex, testType))

class adMatchingTest(unittest.TestCase):
	def test_getDataset(self):
		result = PM.getDataset(sDate, eDate, testIndex, testType)
		print(result)




def suite():
	suite = unittest.TestSuite()
	# suite.addTest(caClusteringTest('test_getDateRange'))
	# suite.addTest(caClusteringTest('test_getDataset'))
	suite.addTest(adMatchingTest('test_getDataset'))
	return suite

if __name__ == "__main__":
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())