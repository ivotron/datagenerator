import re

class Instance():
   """An instance corresponds to a set of features and set of labels
   """
   def __init__(self, number, features, labels):
      """
      Args:
         number (int): the instance number (or ID)
         features (list): a :class:`Feature` list
         labels (list): a :class:`Label` list
      """
      self.number = number
      self.features = features
      self.labels = labels
      self.items = features + labels
      self.itemValues = [None] * (len(self.labels) + len(self.features))

   def size(self):
      return self.items.size

   def assign(self, item, value):
      """
         Assigns the given feature with the given value.

         Args:
            feature (Feature): the feature being assigned

         Raises:
            Exception: if the feature isn't in this instance's feature list or
                       if the feature has been already assigned with a value

         TODO:
            - validate the assignment with the data type, eg. if an attribute
            - this method is needless, use a dictionary for items (with 
                  features/values as keys) and remove it (as well as `value`)
      """
      if item not in self.items:
         raise Exception("item " + str(item) + " not in list of items")

      n = self.items.index(item)

      if self.itemValues[n] != None:
         raise Exception(
               "item " + str(item) + " already assigned with " + 
               str(self.itemValues[n]))

      self.itemValues[n] = value

   def value(self, item):
      """
         Returns the value of the given feature or label.

         Args:
            item (Feature or Label): the feature or label being retrieved

         Raises:
            Exception: if the item isn't in this instance's feature list or
                       if the item has not been already assigned with a value
      """
      if item not in self.items:
         raise Exception("item " + str(item) + " not in list of items")

      n = self.items.index(item)

      if self.itemValues[n] == None:
         raise Exception("item " + str(item) + " not assigned")

      return self.itemValues[n]

class InstanceItem():
   def __init__(self, name, dataType, distribution):
      """Creates a member of an instance.

      Args:
         name (str): name associated to the item
         dataType (DataType): an instance of :class:`DataType`
         distribution (Distribution): an instance of :class:`Distribution`
      """
      self.name = name
      self.dataType = dataType
      self.distribution = distribution

   def __eq__(self, other):
      return self.dataType == other.dataType and \
             self.name == other.name and \
             self.distribution == other.distribution

class Feature(InstanceItem):
   pass

class Label(InstanceItem):
   pass

class DataType():
   def __init__(self, spec):
      """Creates a data type.

      Args:
         spec (str): valid data types specifications are::

            int32       -- 4-byte integer
            string(n)   -- an n-th character string (UTF-8)
            binary(n)   -- an n-th bit binary value
            conditional --
            int(n)      -- an integer in the [0, n] range

      Raises:
         Exception: if the type is not of the ones specified :class:`Exception`

      """

      if "string" in spec:
         self.name = "string"
         self.size = DataType.extractSize(spec)
         self.values = None
      elif "binary" in spec:
         self.name = "binary"
         self.size = DataType.extractSize(spec)
         self.values = None
      elif spec == "int32":
         self.name = "int32"
         self.size = 1
         self.values = None
      elif "int" in spec:
         self.name = "int"
         self.size = 1
         self.values = DataType.extractSize(spec) + 1
      elif spec == "conditional":
         self.name = "conditional"
         self.size = 1
         self.values = None
      elif "value_list" in spec:
         self.name = "value_list"
         self.values = DataType.extractValues(spec)
         if len(self.values) == 0:
            raise Exception("'value_list' data type expects at least one value")
         self.size = len(max(self.values, key=len))
      else:
         raise Exception("unknown data type " + spec)

   def __eq__(self, other):
      return self.name == other.name and \
             self.size == other.size and \
             self.values == other.values

   @staticmethod
   def extractSize(dataType):
      """Exctracts the size of a data type

      Args:
         dataType (str): a string followed by an integer inside parenthesis::

                            sometype(n) -- where n is the size

      Raises:
          Exception: if the format is wrong

      """
      sizeFinder = re.compile('\((\d+)\)')
      n = sizeFinder.findall(dataType)

      if len(n) != 1:
         raise Exception("invalid size specification in '"+dataType+"'")

      return int(n[0])

   @staticmethod
   def extractValues(dataType):
      """Exctracts the list of values given as the specification of a type

      Args:
         spec (str): a string followed by a value list inside parenthesis::

                            sometype(val1,val2,val3)

      Raises:
          Exception: if the format is wrong

      """
      sizeFinder = re.compile('(\w+,?)+')

      vals = sizeFinder.findall(dataType)
      valsWithoutComma = []

      for value in vals[1:len(vals)]: # ignore first
         valsWithoutComma.append(value.translate(None, ","))

      return valsWithoutComma

class Distribution():
   def __init__(self, name):
      """Creates a distribution

      Args:
         distribution (str): valid types are::

            uniform --
            gamma   --
            beta    --
            conditional --

      Raises:
         Exception: if the type is not of the ones specified :class:`Exception`

      """

      if name != "uniform" and \
         name != "gamma" and \
         name != "beta" and \
         name != "conditional" and \
         name != "log-normal":
         raise Exception("unknown distribution type " + name)

      self.name = name
      self.parameters = {}

      # TODO: define subclasses for each data type or alternatively, generic 
      # parameters (eg. parameter1, paremeter2, etc.) where the meaning of each 
      # depends on the distribution type

   def __eq__(self, other):
      return self.name == other.name

   def addParameter(self, parameterNumber, value):
      self.parameters[parameterNumber] = value
