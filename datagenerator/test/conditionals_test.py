from datagenerator.generation import Configuration
from datagenerator.generation import InstanceGenerator

from math import floor
from os import remove
from unittest import TestCase

class rangeConditionalTest(TestCase):

   def test_basic(self):
      """
         Checks a basic example with only two buckets
      """
      confFile = open('conf/temp.conf', 'w')

      confFile.write("""
[global]

data_points = 100

features = 1
feature_1_type = int32
feature_1_distribution = uniform

labels = 1
label_1_type = binary(1)
label_1_distribution = conditional
label_1_parameter1 = rangeConditional
label_1_parameter2 = '{ "instanceMembers": [1], "bucketSize": 2147483648, "values": [0,1] }'

output = csv
output_file = output.csv

      """)
      confFile.close()

      conf = Configuration('conf/temp.conf')
      ig = InstanceGenerator(conf)

      for _ in range(10):
         i = ig.generateNext()

         feature = i.value(conf.features[0])
         label = i.value(conf.labels[0])

         if feature < 0:
            self.assertEqual(label, 0)
         else:
            self.assertEqual(label, 1)

      remove('conf/temp.conf')

      #########################################

      confFile = open('conf/temp.conf', 'w')

      confFile.write("""
[global]

data_points = 100

features = 1
feature_1_type = int32
feature_1_distribution = uniform

labels = 1
label_1_type = binary(1)
label_1_distribution = conditional
label_1_parameter1 = rangeConditional
label_1_parameter2 = '{ "instanceMembers": [1], "bucketSize": 536870912, "values": [0,1,1,1,1,1] }'

output = csv
output_file = output.csv
      """)
      confFile.close()

      conf = Configuration('conf/temp.conf')
      ig = InstanceGenerator(conf)

      for _ in range(10):
         i = ig.generateNext()

         feature = i.value(conf.features[0])
         label = i.value(conf.labels[0])

         if int((floor(feature + 2147483648) / 536870912) % 6) == 0:
            self.assertEqual(label, 0)
         else:
            self.assertEqual(label, 1)

      remove('conf/temp.conf')
