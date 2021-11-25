"""
This is just a place holder, 
I think there will be different tests files 
for different parts of the application 
"""

# ############# Unit tests ##############
import unittest

class MyTestCase(unittest.TestCase):
	def test_something(self):
		self.assertEqual(True,False)  # add assertion here


# ########## Regression tests ###########
import test


if __name__ == '__main__':
	unittest.main()
