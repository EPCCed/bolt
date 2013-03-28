import unittest
import os
import sys
from job import Job
from batch import Batch
from resource import Resource

configDir = "/unittest/configuration"
batchConfig = "test.batch"
resourceConfig = "test.resource"
    
class JobTestCase(unittest.TestCase):
    
    def setUp(self):
        self.job = Job()
        self.batch = Batch()
        self.Resource = Resource()
        
        rootDir = os.environ['BOLT_DIR']
        self.batch.readConfig(rootDir + configDir + "/" + batchConfig)
        self.resource.readConfig(rootDir + configDir + "/" + resourceConfig)

    def testParallelTaskDitributionPureMPI(self):
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(resource.numCoresPerNode())
        self.job.setThreads(1)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        sys.stdout.write("Pure MPI distribution...")
        correct = "aprun -n 1024 -N 32 -S 8 -d 1"
        assert self.job.runLine == correct, "Pure MPI parallel distribution incorrect = {0} ({1}).".format(self.job.runLine, correct)
        print "OK"
        
    def testParallelTaskDitributionHalfPopulate(self):
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(16)
        self.job.setThreads(1)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        sys.stdout.write("Half populated distribution...")
        correct = "aprun -n 1024 -N 16 -S 4 -d 2"
        assert self.job.runLine == correct, "Half populated parallel distribution incorrect = {0} ({1}).".format(self.job.runLine, correct)
        print "OK"

    def testParallelTaskDitributionTwoThreads(self):
        
        # Set the parallel distribution
        self.job.setTasks(1024)
        self.job.setTasksPerNode(16)
        self.job.setThreads(2)
        self.job.setParallelDistribution(self.resource, self.batch)
        
        sys.stdout.write("Hybrid MPI/OpenMP (2 threads)...")
        correct = "export OMP_NUM_THREADS=2\naprun -n 1024 -N 16 -S 4 -d 2"
        assert self.job.runLine == correct, "Hybrid MPI/OpenMP (2 threads) distribution incorrect = {0} ({1}).".format(self.job.runLine, correct)
        print "OK"
        
if __name__ == "__main__":
    unittest.main()