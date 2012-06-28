#----------------------------------------------------------------------
# Copyright 2012 EPCC, The University of Edinburgh
#
# This file is part of bolt.
#
# bolt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bolt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bolt.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Run tests to verify that bolt is working correctly
#
# This script is dependent on the environment variable $BOLT_DIR
# being set correctly.
#----------------------------------------------------------------------

# Set environment variable to pick up Python modules
export PYTHONPATH=$BOLT_DIR/modules:$PYTHONPATH

nfail=0

# Test 1: Parallel job with fully-populated nodes
#   Uses: HECToR.resource; PBSPro.batch
test="test1"
echo "========================================================"
echo "$test: fully-populated nodes..."
$BOLT_DIR/bin/bolt -r HECToR -b PBSPro -A z01 -j $test -n 1024 -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi

# Test 2: Parallel job with half-populated nodes
#   Uses: HECToR.resource; PBSPro.batch
test="test2"
echo "========================================================"
echo "$test: half-populated nodes with stride of 2..."
$BOLT_DIR/bin/bolt -r HECToR -b PBSPro -A z01 -j $test -n 1024 -N 16 -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi
# Test 3: Serial job
#   Uses: HECToR.resource; PBSPro.batch
test="test3"
echo "========================================================"
echo "$test: serial job..."
$BOLT_DIR/bin/bolt -r HECToR -b PBSPro -A z01 -j $test -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi
# Test 4: Parallel job with a single task
#   Uses: HECToR.resource; PBSPro.batch
test="test4"
echo "========================================================"
echo "$test: parallel job with single task..."
$BOLT_DIR/bin/bolt -r HECToR -b PBSPro -A z01 -p -j $test -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi

# Test 5: Parallel job with fully-populated nodes, 6 hours
#   Uses: HECToR.resource; PBSPro.batch
test="test5"
echo "========================================================"
echo "$test: 6 hour job..."
$BOLT_DIR/bin/bolt -r HECToR -b PBSPro -A z01 -j $test -t 6:0:0 -n 1024 -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi
# Test 6: Parallel job with no job launcher
#   Uses: Huygens2.resource; LL_PPC64.batch
test="test6"
echo "========================================================"
echo "$test: 6 no job launcher, request by nodes..."
$BOLT_DIR/bin/bolt -r Huygens -b LL_PPC64 -j $test -n 256 -o $test.bolt $test &> /dev/null
diff $test.bolt $test.verify &> /dev/null
if [ $? -eq 0 ]; then
        rm $test.bolt
        echo "   ...$test passed."
else
        nfail=`expr $nfail + 1`
        echo "   ...$test failed. Diff:"
        diff $test.bolt $test.verify
fi

if [ $nfail -gt 0 ]; then
        echo
        echo "$nfail test(s) failed"
        echo
else
        echo
        echo "All tests passed"
        echo
fi
