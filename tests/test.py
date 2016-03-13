import unittest
import os
import sys
from temp import answer

# print "xxx",sys.path
# scriptpath = "../answer.py"
# sys.path.append(os.path.abspath(scriptpath))
class SimplisticTest(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()