DataGenerator:

  * take into account more feature types:
      - floating point
      - commond domains: names, ZIP, address, etc.
  * add support for correlated features
  * many things all over the codebase are done redundantly:
      - the calculation of the range for binary numbers (`pow(2, dataType.size)`) can be done in the 
        constructor instead of doing it every time a binary number is generated. By going through 
        all the instance "schema" (i.e. iterate over the `Feature`/`Label` of an instance and 
        calculating it once)
      - the corresponding `ValueGenerator` class can be obtained in advance too (same as above)
      - many validations are done each and everytime a new instance is generated (this can be 
        optimized too)
  * add names to features

Conditionals:

  * when `conditional` is used as the `Distribution` type, it should check whether or not the given 
    class exists, if not, an error will be thrown
  * improve the conditional by allowing any arbitrary piece of code to be loaded (might be dangerous 
    though)
  * in `rangeConditional`, allow more than one single integer (or only-binary) features
  * in `rangeConditional`, support for receiving the number of intervals instead of the bucketSize
  * in `conditionals.py` validate the arguments given via the conf. file. Eg. that args["features"] 
    is a list of numbers
  * make `conditionals.rangeConditional` work on a list of binary features
