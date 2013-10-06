from datagenerator.core import DataType
from datagenerator.core import Distribution
from datagenerator.core import Feature
from datagenerator.core import Instance
from datagenerator.core import Label
from datagenerator.writers import WriterFactory
from datagenerator.test.cases import ExtendedTestCase

from os import remove

class FactoryTest(ExtendedTestCase):

   def test_csv(self):
      # missing 'output_file'
      self.assertRaisesWithMessage(
            "missing 'output_file' argument",
            WriterFactory.create,
            output="csv")

      # OK
      w = WriterFactory.create(output="csv", output_file="somefile")

      self.assertEqual(w.__class__.__name__, "CSVWriter")
      self.assertEqual(w.fileName, "somefile")

class CSVWriterTest(ExtendedTestCase):

   def test_basic(self):
      w = WriterFactory.create(output="csv", output_file="test.csv")

      f1 = Feature("feature_1",DataType("string(128)"), Distribution("uniform"))
      l1 = Label("label_1",DataType("binary(1)"), Distribution("uniform"))

      i = Instance(1, [f1], [l1])

      i.assign(f1, "jorono")
      i.assign(l1, "1")

      w.open()
      w.write(i)
      w.close()

      lines = open('test.csv').readlines()
      self.assertEqual(len(lines), 2)
      self.assertEqual(lines[0], "feature1,label1\n")
      self.assertEqual(lines[1], "jorono,1\n")

      remove("test.csv")

class ARFFWriterTest(ExtendedTestCase):

   def test_basic(self):
      w = WriterFactory.create(output="arff", output_file="test.arff")

      f1 = Feature("feature_1",DataType("int32"), Distribution("uniform"))
      l1 = Label("label_1",DataType("binary(1)"), Distribution("uniform"))

      i = Instance(1, [f1], [l1])

      i.assign(f1, "34")
      i.assign(l1, "1")

      w.open()
      w.write(i)
      w.close()

      lines = open('test.arff').readlines()
      self.assertEqual(len(lines), 6)
      self.assertEqual(lines[0], "@relation synthetic\n")
      self.assertEqual(lines[1], "@attribute feature1 numeric\n")
      self.assertEqual(lines[2], "@attribute label1 {0, 1}\n")
      self.assertEqual(lines[3], "\n")
      self.assertEqual(lines[4], "@data\n")
      self.assertEqual(lines[5], "34,1\n")

      remove("test.arff")
