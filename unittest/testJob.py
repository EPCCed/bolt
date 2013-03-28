import unittest
import os
import sys
from job import Job
    
class JobTestCase(unittest.TestCase):
    
    def setUp(self):
        self.job = Job()

    def testName(self):
        """Set job name"""
        correct = "test"
        self.job.setName(correct)
        self.assertEqual(self.job.name, correct, "Value= '{0}', Expected= '{1}'".format(self.job.name, correct))

    def testParallel(self):
        """Set parallel job"""
        self.job.setIsParallel(True)
        assert self.job.isParallel, "Job is not parallel and should be."
        
def suite():
    suite = unittest.makeSuite(JobTestCase,'test')
    return suite
        
if __name__ == "__main__":
    unittest.main()