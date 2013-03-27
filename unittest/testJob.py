import unittest
import os
from job import Job
from batch import Batch
from resource import Resource
from code import Code

class JobTestCase(unittest.TestCase):
    
    configDir = "/unittest/configuration"
    batchConfig = "test.batch"
    resourceConfig = "test.resource"
    codeConfig = "test.code"

    def setUp(self):
        self.job = Job()

    def testName(self):
        self.job.setName("test")
        assert self.job.name == "test", "Job name not set correctly = '{0}' (should be '{1}').".format(self.job.name, "test")

    def testParallel(self):
        self.job.setIsParallel(True)
        assert self.job.isParallel, "Job is not parallel and should be."

    # Test the distribution of parallel tasks (e.g. pure MPI job)
    def testParallelTaskDitribution(self):
        rootDir = os.environ['BOLT_DIR']
        batch = Batch()
        batch.readConfig(rootDir + configDir + "/" + batchConfig)
        resource = Resource()
        resource.readConfig(rootDir + configDir + "/" + resourceConfig)
        
        self.job.setTasks(1024)
        self.job.setTasksPerNode(resource.numCoresPerNode())
        
        self.job.setParallelDistribution(resource, batch)
        
        
              
        # To test the functionality of the task distribution we need a resource configured. We can do this by re
        # reading a resource configuration file. We probably need to place a resource configuration file
        # in the test directory to make this work. We would also need a batch configuration file???
        
if __name__ == "__main__":
    unittest.main()