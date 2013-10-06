from datagenerator.core import DataType
from datagenerator.core import Distribution
from datagenerator.core import Feature
from datagenerator.core import Instance
from datagenerator.core import Label
from datagenerator.test.cases import ExtendedTestCase
import unittest

class InstanceTest(ExtendedTestCase):

   def test_basic(self):
      f1 = Feature("feature_1",DataType("string(128)"), Distribution("uniform"))
      f2 = Feature("feature_2",DataType("int32"), Distribution("uniform"))
      l1 = Label("label_1",DataType("binary(1)"), Distribution("uniform"))

      fs = [f1]
      ls = [l1]

      i = Instance(1, fs, ls)

      i.assign(f1, "3")

      self.assertEqual(i.value(f1), "3")

      self.assertRaisesWithMessage(
            "item " + str(f2) + " not in list of items", i.assign, f2, "a")
      self.assertRaisesWithMessage(
            "item " + str(l1) + " not assigned", i.value, l1)

class FeatureTest(unittest.TestCase):
   """For Label, the test is exactly the same
   """

   def test_basic(self):
      feature = \
         Feature("feature",DataType("string(128)"), Distribution("uniform"))

      self.assertEqual(feature.dataType, DataType("string(128)"))
      self.assertEqual(feature.distribution, Distribution("uniform"))

class DataTypeTest(unittest.TestCase):

   def test_basic(self):
      feature = DataType("binary(4)")
      self.assertEqual(feature.name, "binary")
      self.assertEqual(feature.size, 4)
      self.assertEqual(feature.values, None)

      feature = DataType("int32")
      self.assertEqual(feature.name, "int32")
      self.assertEqual(feature.size, 1)
      self.assertEqual(feature.values, None)

      feature = DataType("int(1)")
      self.assertEqual(feature.name, "int")
      self.assertEqual(feature.size, 1)
      self.assertEqual(feature.values, 2)

      feature = DataType("int(99)")
      self.assertEqual(feature.name, "int")
      self.assertEqual(feature.size, 1)
      self.assertEqual(feature.values, 100)

      feature = DataType("string(128)")
      self.assertEqual(feature.name, "string")
      self.assertEqual(feature.size, 128)
      self.assertEqual(feature.values, None)

      feature = DataType("value_list(val1, val2, val3)")
      self.assertEqual(feature.name, "value_list")
      self.assertEqual(feature.size, 4)
      self.assertEqual(len(feature.values), 3)

      feature = DataType("value_list(onlyoneValue)")
      self.assertEqual(feature.name, "value_list")
      self.assertEqual(feature.size, 12)
      self.assertEqual(len(feature.values), 1)

      feature = DataType("value_list(distinct, values, withdifferent, size)")
      self.assertEqual(feature.name, "value_list")
      self.assertEqual(feature.size, 13) # size is with respect to longest
      self.assertEqual(len(feature.values), 4)

      # TODO value_list file
      # feature = DataType("value_list(file.txt)")

      self.assertRaises(Exception, DataType, "anything-else")
      self.assertRaises(Exception, DataType, "int()")
      self.assertRaises(Exception, DataType, "int(0,1,2)")
      self.assertRaises(Exception, DataType, "string(")
      self.assertRaises(Exception, DataType, "string(adfdklsaf)")
      self.assertRaises(Exception, DataType, "binary(182)(182)")
      self.assertRaises(Exception, DataType, "value_list")
      self.assertRaises(Exception, DataType, "value_list()")

class DistributionTest(unittest.TestCase):

   def test_basic(self):
      dist = Distribution("uniform")
      self.assertEqual(dist.name, "uniform")
      dist = Distribution("beta")
      self.assertEqual(dist.name, "beta")
      dist = Distribution("gamma")
      self.assertEqual(dist.name, "gamma")
      dist = Distribution("log-normal")
      self.assertEqual(dist.name, "log-normal")

      self.assertRaises(Exception, Distribution, "anything-else")

      # TODO: check parameters for non-uniform distributions

if __name__ == '__main__':
   unittest.main()
