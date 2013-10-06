from random import seed
from random import randint

# OS-based seeding (system time)
seed

class WriterFactory():
   """
      Utility class that creates writers based on their properties.

      For every new writer, we have to add its type in the ``validWriterTypes``
      member variable
   """
   validWriterTypes = 'csv', 'arff'

   @staticmethod
   def create(**kwargs):
      """
         given the properties of a writer, instantiates an object of the
         corresponding class and passes the properties to its constructor
      """
      if not "output" in kwargs:
         raise Exception("missing 'output' argument")

      if kwargs["output"] == "csv":
         return CSVWriter(**kwargs)
      elif kwargs["output"] == "arff":
         return ARFFWriter(**kwargs)
      else:
         raise Exception("unknown writer " + kwargs["output"])

class Writer():
   def __init__(self, **kwargs):
      pass

   def open(self):
      self.outFile = open(self.fileName, 'w')

   def close(self):
      self.outFile.close()

class CSVWriter(Writer):
   def __init__(self, **kwargs):
      if not "output_file" in kwargs:
         raise Exception("missing 'output_file' argument")

      self.fileName = kwargs["output_file"]
      self.separator = ","
      self.includeHeaders = True
      self.wroteHeaders = False

   def write(self, instance):
      # print the header
      if not self.wroteHeaders and self.includeHeaders:
         self.writeHeader(instance)
         self.wroteHeaders = True

      self.writeInstance(instance)

   def writeHeader(self, instance):
      for counter, f in enumerate(instance.features, start=1):
         self.outFile.write(
            'feature' + str(counter) + self.separator)

      for counter, l in enumerate(instance.labels, start=1):
         self.outFile.write('label' + str(counter))
         if counter < len(instance.labels):
            self.outFile.write(self.separator)

      self.outFile.write('\n')

   def writeInstance(self, instance):
      # print the instance
      for counter, f in enumerate(instance.features, start=1):
         self.outFile.write(str(instance.value(f)) + self.separator)

      for counter, l in enumerate(instance.labels, start=1):
         self.outFile.write(str(instance.value(l)))
         if counter < len(instance.labels):
            self.outFile.write(self.separator)

      self.outFile.write('\n')

class ARFFWriter(Writer):
   def __init__(self, **kwargs):
      if not "output_file" in kwargs:
         raise Exception("missing 'output_file' argument")

      self.fileName = kwargs["output_file"]
      self.separator = ","
      self.wroteHeader = False

   def write(self, instance):
      # print the header
      if not self.wroteHeader:
         self.writeHeader(instance)
         self.wroteHeader = True

      self.writeInstance(instance)

   def writeHeader(self, instance):
      self.outFile.write('@relation synthetic\n')

      for counter, f in enumerate(instance.features, start=1):
         self.outFile.write('@attribute feature' + str(counter))
         if f.dataType.name == "int32":
            self.outFile.write(' numeric')
         else:
            raise Exception("Unsupported data type " + f.dataType.name)
         self.outFile.write('\n')

      for counter, l in enumerate(instance.labels, start=1):
         self.outFile.write('@attribute label' + str(counter))
         if l.dataType.name == "binary":
            self.outFile.write(' {0, 1}')
         else:
            raise Exception("Unsupported data type " + l.dataType.name)
         self.outFile.write('\n\n')

      self.outFile.write('@data\n')

   def writeInstance(self, instance):
      # print the instance
      for counter, f in enumerate(instance.features, start=1):
         self.outFile.write(str(instance.value(f)) + self.separator)

      for counter, l in enumerate(instance.labels, start=1):
         self.outFile.write(str(instance.value(l)))
         if counter < len(instance.labels):
            self.outFile.write(self.separator)

      self.outFile.write('\n')
