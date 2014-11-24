import unittest
import os
from boltjob import BoltJob as Job
from boltbatch import BoltBatch as Batch
from boltresource import BoltResource as Resource

configDir = "/unittest/configuration"
batchConfig = "test.batch"
resourceConfig = "test.resource"
    
class DistributionTestCase(unittest.TestCase):
    
    def setUp(self):
        self.job = Job()
        self.batch = Batch()
        self.resource = Resource()
        
        rootDir = os.environ['BOLT_DIR']
        self.batch.readConfig(rootDir + configDir + "/" + batchConfig)
        self.resource.readConfig(rootDir + configDir + "/" + resourceConfig)

    def testParallelTaskDitributionPureMPI(self):
        """Pure MPI task distribution (fully populated)."""
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(self.resource.numCoresPerNode())
        self.job.setThreads(1)
        self.job.setParallelJobLauncher(self.resource.distribJobLauncher)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        correct = "aprun -n 1024 -N 32 -S 8 -d 1"
        self.assertEqual(self.job.runLine, correct, "Value= '{0}', Expected= '{1}'".format(self.job.runLine, correct))
        
    def testParallelTaskDitributionHalfPopulate(self):
        """Pure MPI task distribution (half populated)."""
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(16)
        self.job.setThreads(1)
        self.job.setParallelJobLauncher(self.resource.distribJobLauncher)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        correct = "aprun -n 1024 -N 16 -S 4 -d 2"
        self.assertEqual(self.job.runLine, correct, "Value= '{0}', Expected= '{1}'".format(self.job.runLine, correct))

    def testParallelTaskDitributionTwoThreads(self):
        """Hybrid MPI/OpenMP task distribution (2 OpenMP threads)."""
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(16)
        self.job.setThreads(2)
        self.job.setParallelJobLauncher(self.resource.hybridJobLauncher)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        correct = "export OMP_NUM_THREADS=2\naprun -n 1024 -N 16 -S 4 -d 2"
        self.assertEqual(self.job.runLine, correct, "Value= '{0}', Expected= '{1}'".format(self.job.runLine, correct))

    def testParallelTaskDitributionThreeThreads(self):
        """Hybrid MPI/OpenMP task distribution (3 OpenMP threads)."""
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(10)
        self.job.setThreads(3)
        self.job.setParallelJobLauncher(self.resource.hybridJobLauncher)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        correct = "export OMP_NUM_THREADS=3\naprun -n 1024 -N 10 -d 3"
        self.assertEqual(self.job.runLine, correct, "Value= '{0}', Expected= '{1}'".format(self.job.runLine, correct))

def suite():
    suite = unittest.makeSuite(DistributionTestCase,'test')
    return suite
        
if __name__ == "__main__":
    unittest.main()
