import unittest

class ExtendedTestCase(unittest.TestCase):
   def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
      # taken from: http://stackoverflow.com/q/8672754/389188
      try:
         func(*args, **kwargs)
         self.fail()
      except Exception as inst:
         self.assertEqual(inst.message, msg)
