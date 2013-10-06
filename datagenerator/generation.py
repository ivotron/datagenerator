from datagenerator.core import DataType
from datagenerator.core import Distribution
from datagenerator.core import Feature
from datagenerator.core import Instance
from datagenerator.core import Label

from datagenerator.writers import WriterFactory

import conditionals

from ast import literal_eval
from ConfigParser import RawConfigParser
from functools import partial
from random import seed
from random import getrandbits
from random import randint

# OS seed
seed

class Configuration():
   """Configuration that the generator reads
   """

   def __init__(self, configFile):
      """Reads a configuration file and sets the configuration based on its
         contents

      Args:
         configFile (str): data generation configuration. For samples see the
                           ``conf`` folder

      """
      self.parseConfigurationFile(configFile)

   def parseConfigurationFile(self, configFile):
      """Reads a configuration file and sets the configuration values based on
         its contents

      Args:
         configFile (str): data generation configuration. For samples see the
                           ``conf`` folder

      Raises:
         Exception: if the configuration is in a bad shape (check examples)

      """
      parser = Configuration.validate(configFile)

      self.dataPoints = parser.getint('global', 'data_points')

      self.features = []
      self.labels = []

      featuresToRead = parser.getint('global', 'features')
      labelsToRead = parser.getint('global', 'labels')

      if featuresToRead is 0 or labelsToRead is 0:
         raise Exception(
               "At least one feature and one label has to be provided")

      self.readTypeAndDistribution(parser, "feature", featuresToRead)
      self.readTypeAndDistribution(parser, "label", labelsToRead)
      self.readOutputType(parser)
      self.parser = parser

   def readTypeAndDistribution(self, parser, whatToRead, numOfItems):
      """Reads the types and distribution of each item

      Args:
         parser (:class:`RawConfigParser`): a parser from :mod:`ConfigParser`
         whatToRead (str): "type" or "distribution"
         numOfItems (int): how many items to read

      Raises:
         Exception: if the configuration is in a bad shape (check examples)

      """
      if whatToRead != "feature" and whatToRead != "label":
         raise Exception("Unknown item to read: " + whatToRead)

      for i in range(0, numOfItems):
         # read data type
         option = whatToRead + "_" + str(i+1) + "_type"

         if not parser.has_option('global', option):
            raise Exception(
                  "expecting datatype for " + whatToRead + " " + str(i+1))

         dataType = DataType(parser.get('global', option))

         # read distribution
         option = whatToRead + "_" + str(i+1) + "_distribution"

         if not parser.has_option('global', option):
            raise Exception(
                  "expecting distribution for " + whatToRead + " " + str(i+1))

         distribution = Distribution(parser.get('global', option))

         Configuration.readDistributionParameters(
               parser, whatToRead, i+1, distribution)

         if whatToRead == "feature":
            self.features.append(
                  Feature("feature_" + str(i), dataType, distribution))
         else:
            self.labels.append(
                  Label("label_" + str(i), dataType, distribution))


   @staticmethod
   def readDistributionParameters(parser, whatToRead, attrNum, distribution):
      """Reads the parameters of a distribution. These are specified by the
         following pattern::

            whatToRead_attrNum_distribution_parameterN

         where the values that `N` takes depend on the distribution being read.

      Args:
         parser (RawConfigParser): a parser from :mod:`ConfigParser`
         whatToRead (str): "type" or "distribution"
         attrNum (int): attribute number to read
         distribution (Distribution): object whose members are being populated

      Raises:
         Exception: if the configuration is in a bad shape (check examples)

      """
      numOfParameters = 0
      if distribution.name == "conditional" or \
         distribution.name == "beta" or \
         distribution.name == "gamma" or \
         distribution.name == "log-normal":
         numOfParameters = 2

      for i in range(0,numOfParameters):
         option = whatToRead + "_" + str(attrNum) + "_parameter" + str(i+1)

         if not parser.has_option('global', option):
            raise Exception(
                  "no distribution parameter: " + str(i+1) + " for " +
                  whatToRead + ": " + str(attrNum))

         parameter = parser.get('global', option)

         distribution.addParameter(i, parameter)


      # TODO: read other parameters for other distributions

   def readOutputType(self, parser):
      """Reads the type of output and filename of output. Valid values is
         ``csv`` or ``arff``.

      Raises:
         Exception: if the output type is distinct to the valid types

      """
      option = parser.get('global', 'output')
      if option not in WriterFactory.validWriterTypes:
         raise Exception("invalid output type: " + option)

      self.output = option

      if not parser.has_option('global', 'output_file'):
         raise Exception("no output file specified")

      self.outputFile = parser.get('global', 'output_file')

   @staticmethod
   def validate(configFile):
      """Validates that a configuration file is correct. For an example of a
         correctly written file, look at ``conf/sample.conf``

      Args:
         parser (:class:`RawConfigParser`): a parser from :mod:`ConfigParser`

      """
      parser = RawConfigParser()
      parser.read(configFile)

      if not parser.has_section('global'):
         raise Exception("missing 'global' section")
      if not parser.has_option('global', 'data_points'):
         raise Exception("missing 'data_points' option")
      if not parser.has_option('global', 'features'):
         raise Exception("missing 'features' option")
      if not parser.has_option('global', 'labels'):
         raise Exception("missing 'features' option")
      if not parser.has_option('global', 'output'):
         raise Exception("missing 'output' option")

      return parser

class DataGenerator():
   @staticmethod
   def generate(confFile):
      c = Configuration(confFile)
      g = InstanceGenerator(c)
      w = WriterFactory.create(**dict(c.parser.items('global')))

      w.open()
      for _ in range(c.dataPoints):
         w.write(g.generateNext())
      w.close()


class InstanceGenerator():
   def __init__(self, config):
      """Creates an instance generator with given configuration

      Args:
         config (Configuration): initial configuration.

      """
      self.config = config
      self.counter = 0

   def generateNext(self):
      """A next instance that complies with the specification given in the
         config file.
      """
      self.current = Instance(
            self.counter, self.config.features, self.config.labels)

      for f in self.config.features:
         self.current.assign(f, self.generate(f.dataType, f.distribution))

      for l in self.config.labels:
         # it's important that the features get generated first: labels with
         # 'conditional' distribution depend on all features being present
         self.current.assign(l, self.generate(l.dataType, l.distribution))

      self.counter += 1

      return self.current

   def generate(self, dataType, distribution):
      return ValueGenerator.getFunction(distribution)(dataType, self.current)

class ValueGenerator():
   """
      Utility class that generate values in their string representation.
   """

   @staticmethod
   def getFunction(distribution):
      """
         Returns the corresponding function for given distribution given

      Args:
         distribution (Distribution): the distribution for which the random
                                      generator function is returned
      """
      if distribution.name == "uniform":
         return ValueGenerator.generateUniform
      elif distribution.name == "beta":
         return partial(ValueGenerator.generateBeta, distribution.parameters)
      elif distribution.name == "conditional":
         conditionalName = distribution.parameters[0]
         conditionalFunc = getattr(conditionals, conditionalName)
         conditionalArgs \
            = literal_eval(str(literal_eval(distribution.parameters[1])))

         return partial(conditionalFunc, conditionalArgs)
      else:
         raise Exception("unsupported distribution " + distribution.name)

   @staticmethod
   def generateUniform(dataType, instance=None):
      """
         Generates values from a uniform distribution
      """
      print "generating value of type " + dataType.name
      if dataType.name == "binary":
         return "{0:b}".format(getrandbits(dataType.size))
      elif dataType.name == "int32":
         return randint(-2147483648, 2147483647)
      elif dataType.name == "int":
         return randint(0, dataType.values)
      elif dataType.name == "value_list":
         r = randint(0, len(dataType.values)-1)
         print "   value list " + ('[%s]' % ', '.join(map(str, dataType.values)))
         print " generated index: " + str(r)
         print " generated value: " + dataType.values[r]
         return dataType.values[r]
      else:
         raise Exception("data type " + dataType.name + " not supported yet")

   @staticmethod
   def generateBeta(parameters, dataType, instance=None):
      """
         Generates values from a uniform distribution
      """
      if dataType.name == "binary":
         raise Exception("can't handle binary yet")
      elif dataType.name == "int32":
         raise Exception("can't handle integers yet")
      else:
         raise Exception("data type " + dataType.name + " not supported yet")
