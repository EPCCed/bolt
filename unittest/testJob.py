import unittest
from job import Job

class JobTestCase(unittest.TestCase):
    def setUp(self):
        self.job = Job()
    def testName(self):
        self.job.setName("test")
        assert self.job.name == "test", "Job name not set correctly = '{0}' (should be '{1}').".format(self.job.name, "test")
    def testParallel(self):
        self.job.setIsParallel(True)
        assert self.job.isParallel, "Job is not parallel and should be."
        
        # To test the functionality of the task distribution we need a resource configured. We can do this by re
        # reading a resource configuration file. We probably need to place a resource configuration file
        # in the test directory to make this work. We would also need a batch configuration file???
        
if __name__ == "__main__":
    unittest.main()