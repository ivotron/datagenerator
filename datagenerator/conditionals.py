from random import random
from math import floor

"""
   Every function defined here gets provided with the same arguments. The
   arguments that a function receives can get extended by inserting entries in
   the ``args`` dictionary. The documentation of each function describes the
   arguments that receives through this dictionary, as well as its logic. This
   global documentation describes the common parameters to all the conditional
   functions defined in this module.

   Args:
      args (dict):
         a dictionary containing the following entries:

      dataType (DataType):
         the data type of the value that is getting conditionally generated

      instance (Instance):
         the instance to which the generated value will be added. It is used to
         access other items in the instance that determine how this
"""

def dummyConditional(args, dataType, instance):
   # does nothing ; used for testing
   pass

def rangeConditional(args, dataType, instance):
   """
      Generates a value based on ranges that are determined by the given
      parameters. The number of ranges (a.k.a. buckets or intervals) are
      specified through the ``"intervals"`` entry in the dictionary. The
      instance members that the condition apply to are specified by the
      ``"instanceMembers"`` entry. .

      Args:

      "instanceMembers" (list):
         currently only one instance member can be specified. More than one can 
         be specified as long as all of them are ``binary``, in which case the 
         range gets determined by aggregating all the bits (in the order they 
         are specified in the list) and constructing a single decimal value, for
         which the ranges are then considered

      "bucketSize" (int):
         when the value range of an instance member is ordered in ascending way,
         the number of elements that each bucket has. **NOTE**: cannot be used 
         in conjunction with "intervals"

      "intervals" (int):
         the number of ranges that are obtained for the specified feature list.
         The ranges are constructed from ascending to ascending order. In
         general, the size of each buckets is obtained by:

            (MAX-MIN / intervals).

         For example, given an 32-bit integer and 4 intervals, then there will
         be four buckets:

             * [-2147483648, -1073741824]
             * [-1073741824, 0]
             * [0, 1073741824]
             * [0, 2147483647]

      "values" (list):
         a list containing values that get assigned in a "round-robin" fashion.
         For example, if the data type being generated is binary, then a
         possible pattern list is the following:

            [0,1,1,0,1]

         For example, for a 5-bit integer, if we have a bucket size of 3, then:

            -16 \
            -15  0
            -14 /
            -13 \
            -12  1
            -11 /
            -10 \
             -9  2
             -8 /
             -7 \
             -6  3
             -5 /
             -4 \
             -3  4
             -2 /
             -1 \
              0  5
              1 /
              ...
              ...
             14 \
             15  11

         that is, we'll have 11 buckets, the last one having 2 values (instead
         of 3). Then, by ordering the buckets in ascending order we can map
         these values in a modular (or round-robin) way to the list of values::

            -16 \
            -15  0 -> 0
            -14 /
            -13 \
            -12  1 -> 1
            -11 /
            -10 \
             -9  2 -> 1
             -8 /
             -7 \
             -6  3 -> 0
             -5 /
             -4 \
             -3  4 -> 1
             -2 /
             -1 \
              0  5 -> 0  <<< loop through the list
              1 /
              ...
              ...
             11 \
             12  9 -> 1
             13 /
             14 \
             15 10 -> 0 <<< loop through the list

      In that way, the buckets get mapped to the assigned values in order. 
      **NOTE**: this argument cannot be used in conjunction with 
      "bernoulli_parameters"

      "bernoully_parameters" (list): list fo...

      Raises:

      Exception:
         if one of the arguments is not given; if the ``values`` list
         contains values that don't correspond to the ``dataType`` being
         generated; if ``instanceMembers`` contains incorrect indexes; if
         ``bucketSize`` is greater than the balue range; if an argument clash 
         occurs

   """
   ## validate arguments

   if args.get("instanceMembers") is None:
      raise Exception("missing 'columns' in rangeConditional args")
   if args.get("bucketSize") is None:
      raise Exception("missing 'bucketSize' in rangeConditional args")
   if args.get("values") is None:
      raise Exception("missing 'values' in rangeConditional args")

   if len(args["instanceMembers"]) is not 1:
      raise Exception("only one element allowed in the 'instanceMembers' list")

   instanceItemIndex = args["instanceMembers"][0] - 1

   if instanceItemIndex > instance.size or instanceItemIndex < 0:
      raise Exception(
            "item index must be in the [1, instance.size] range: " + 
            str(instanceItemIndex))

   bucketSize = args["bucketSize"]
   maxValue = 2147483648 # TODO: to generalize, replace by a getMax()
                         #       that works on binaries too

   if (bucketSize > (maxValue * 2)):
      raise Exception("'bucketSize' greater than maximum int value range")

   if type(bucketSize) is not int:
      raise Exception("'bucketSize' should be integer")

   ########
   # the actual conditional generation, in 4 simple steps (assumes integers only)
   ########

   # 1. get the value we're conditioning on
   itemValue = instance.value(instance.items[instanceItemIndex])

   # 2. shift the range (make all numbers positive)
   itemValue += maxValue

   # 3. obtain the bucket number (or bucket ID)
   bucketNumber = floor(itemValue / bucketSize)

   # 4. get the corresponding member from the values list
   indexOfAssignmentValue = int(bucketNumber % len(args["values"]))

   return args["values"][indexOfAssignmentValue]

def rangeForBinaryWithBernoulliParameterConditional(args, dataType, instance):
   """
      Can only be applied to binary members of the instance ("instanceMembers")

      values (list) : a list of values in the range [0,1) that describe the 
                      bernoulli parameter used to generate a random value
   """
   if args.get("instanceMembers") is None:
      raise Exception("missing 'columns' in rangeConditional args")
   if args.get("bucketSize") is None:
      raise Exception("missing 'bucketSize' in rangeConditional args")
   if args.get("values") is None:
      raise Exception("missing 'values' in rangeConditional args")

   if len(args["instanceMembers"]) is not 1:
      raise Exception("only one element allowed in the 'instanceMembers' list")

   instanceItemIndex = args["instanceMembers"][0] - 1

   if instanceItemIndex > instance.size or instanceItemIndex < 0:
      raise Exception(
            "item index must be in the [1, instance.size] range: " + 
            str(instanceItemIndex))

   bucketSize = args["bucketSize"]
   maxValue = 2147483648 # TODO: to generalize, replace by a getMax()
                         #       that works on binaries too

   if (bucketSize > (maxValue * 2)):
      raise Exception("'bucketSize' greater than maximum int value range")

   if type(bucketSize) is not int:
      raise Exception("'bucketSize' should be integer")

   itemValue = instance.value(instance.items[instanceItemIndex])
   itemValue += maxValue
   bucketNumber = floor(itemValue / bucketSize)
   indexOfAssignmentValue = int(bucketNumber % len(args["values"]))

   p = args["values"][indexOfAssignmentValue]

   if random() < p:
      return 1
   else:
      return 0
