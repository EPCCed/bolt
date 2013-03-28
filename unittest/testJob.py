import unittest
import os
import sys
from job import Job
    
class JobTestCase(unittest.TestCase):
    
    def setUp(self):
        self.job = Job()

    def testName(self):
        correct = "test"
        self.job.setName(correct)
        sys.stdout.write("Set job name...")
        assert self.job.name == correct, "Job name not set correctly = '{0}' (should be '{1}').".format(self.job.name, correct)
        print "OK"

    def testParallel(self):
        self.job.setIsParallel(True)
        sys.stdout.write("Set parallel job...")
        assert self.job.isParallel, "Job is not parallel and should be."
        print "OK"
        
if __name__ == "__main__":
    unittest.main()