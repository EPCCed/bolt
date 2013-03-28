import unittest
import os
from job import Job
from batch import Batch
from resource import Resource
from code import Code

configDir = "/unittest/configuration"
batchConfig = "test.batch"
resourceConfig = "test.resource"
codeConfig = "test.code"
    
class JobTestCase(unittest.TestCase):
    
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
        # Read the configuration files
        rootDir = os.environ['BOLT_DIR']
        batch = Batch()
        batch.readConfig(rootDir + configDir + "/" + batchConfig)
        resource = Resource()
        resource.readConfig(rootDir + configDir + "/" + resourceConfig)
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(resource.numCoresPerNode())
        self.job.setThreads(1)
        self.job.setParallelDistribution(resource, batch)
        
        assert self.job.runLine == "aprun -n 1024 -N 32 -S 8 -d 1", "Pure MPI parallel distribution incorrect."
        
if __name__ == "__main__":
    unittest.main()