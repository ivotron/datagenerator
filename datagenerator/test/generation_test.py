from datagenerator.core import DataType
from datagenerator.core import Distribution
from datagenerator.generation import Configuration
from datagenerator.generation import InstanceGenerator
from datagenerator.generation import ValueGenerator
from datagenerator.test.cases import ExtendedTestCase

import unittest
import os

class ConfigurationTest(ExtendedTestCase):

   def setUp(self):
      self.messedConfFile = 'conf/messed.conf'

   def test_goodFile(self):
      conf = Configuration('conf/sample.conf')

      self.assertEqual(conf.dataPoints, 100)
      self.assertEqual(len(conf.features), 1)
      self.assertEqual(len(conf.labels), 1)
      self.assertEqual(conf.output, "csv")
      self.assertEqual(conf.outputFile, "output.csv")

   def test_basic(self):

      # empty
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('')
      confFile.close()

      self.assertRaises(Exception, Configuration.validate, self.messedConfFile)

      # no labels
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.close()

      self.assertRaises(Exception, Configuration.validate, self.messedConfFile)

      # no data points
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.close()

      self.assertRaises(Exception, Configuration.validate, self.messedConfFile)

      # no features
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('labels = 1\n')
      confFile.close()

      self.assertRaises(Exception, Configuration.validate, self.messedConfFile)

      # missing output
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.close()

      self.assertRaises(Exception, Configuration.validate, self.messedConfFile)

      # OK
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.close()

      Configuration.validate(self.messedConfFile)
      os.remove(self.messedConfFile)

   def test_dataTypes(self):

      self.messedConfFile = 'conf/messed.conf'

      # no feature type
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "expecting datatype for feature 1",
            Configuration,
            self.messedConfFile)

      # no feature distribution
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "expecting distribution for feature 1",
            Configuration,
            self.messedConfFile)

      # no label type
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "expecting datatype for label 1",
            Configuration,
            self.messedConfFile)

      # no label distribution
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "expecting distribution for label 1",
            Configuration,
            self.messedConfFile)

      # missing parameters (conditional labeling)
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = binary(1)\n')
      confFile.write('label_1_distribution = conditional\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "no distribution parameter: 1 for label: 1",
            Configuration,
            self.messedConfFile)

      # OK
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('output_file = somefilename\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      Configuration(self.messedConfFile)
      os.remove(self.messedConfFile)

      # TODO:
      #  * gamma, beta, log-normal
      #  * parameters for each of the above

   def test_output(self):

      self.messedConfFile = 'conf/messed.conf'

      # bad output type
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = otherthancsv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "invalid output type: otherthancsv",
            Configuration,
            self.messedConfFile)

      # no filename for output
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      self.assertRaisesWithMessage(
            "no output file specified",
            Configuration,
            self.messedConfFile)

      # OK
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = csv\n')
      confFile.write('output_file = somefilename\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      Configuration(self.messedConfFile)

      # OK
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = arff\n')
      confFile.write('output_file = somefilename\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      Configuration(self.messedConfFile)

      # OK
      os.remove(self.messedConfFile)
      confFile = open(self.messedConfFile, 'w')
      confFile.write('[global]\n')
      confFile.write('data_points = 100\n')
      confFile.write('features = 1\n')
      confFile.write('labels = 1\n')
      confFile.write('output = mr\n')
      confFile.write('output_file = somefilename\n')
      confFile.write('feature_1_type = binary(2)\n')
      confFile.write('feature_1_distribution = uniform\n')
      confFile.write('label_1_type = int32\n')
      confFile.write('label_1_distribution = beta\n')
      confFile.write('label_1_parameter1 = one\n')
      confFile.write('label_1_parameter2 = two\n')
      confFile.close()

      Configuration(self.messedConfFile)
      os.remove(self.messedConfFile)

class InstanceGeneratorTest(unittest.TestCase):

   def test_basic(self):
      conf = Configuration('conf/sample.conf')
      ig = InstanceGenerator(conf)

      i = ig.generateNext()

      self.assertEqual(i.number, 0)
      self.assertEqual(i, ig.current)

      i = ig.generateNext()

      self.assertEqual(i.number, 1)
      self.assertEqual(i, ig.current)

class ValueGeneratorTest(ExtendedTestCase):
   def test_functionSearch(self):
      d = Distribution("uniform")
      self.assertEqual(
            ValueGenerator.getFunction(d), ValueGenerator.generateUniform)
      d = Distribution("conditional")
      d.addParameter(0, "dummyConditional")
      d.addParameter(1, "{'foo' : 3 , 'bar' : 5 }")
      self.assertEqual(
            ValueGenerator.getFunction(d).__class__.__name__, "partial")

   def test_uniformGenerator(self):
      dt = DataType("binary(2)")

      value = ValueGenerator.generateUniform(dt)

      # check binary
      self.assertTrue(len(value) > 0 and len(value) <= 2)
      self.assertTrue("0" in value or "1" in value)
      self.assertTrue("2" not in value)
      self.assertTrue("3" not in value)
      self.assertTrue("4" not in value)
      self.assertTrue("5" not in value)
      self.assertTrue("6" not in value)
      self.assertTrue("7" not in value)
      self.assertTrue("8" not in value)
      self.assertTrue("9" not in value)

      # check integer
      dt = DataType("int32")

      value = ValueGenerator.generateUniform(dt)

      int(value) # this will throw an exception if value is not a proper integer


   def test_stringGenerator(self):
      # TODO: test for string, eg. "string(10)" is a 10 character string
      pass

   """
class GeneratorTest(unittest.TestCase):

   def test_basic(self):
      generator = Generator(Configuration('conf/sample.conf'))

      generator.generate

      #csvOut = open('output.csv')

      numLines = sum(1 for line in open('output.csv'))
      self.assertEqual(numLines, 101) # points + header
   """

if __name__ == '__main__':
    unittest.main()
