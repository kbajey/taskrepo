"""
This module consists all the necessary code for converting a numeric type to short scale format.
The short scale format supports millions, billions and trillions for the current release. The 
extensions for short scale viz. Quadrillion(P), Quintillion(E), Sextillion(Z), Septillion(Y) can
be done by adding the suffices to suffix array and digits dictionary.

Other formats of representing large numbers can be done by extending class NumberPrettify and
implement the algorithm for representing the new scheme of large numbers. Update the factory class
to support the new class.
"""

__author__ = "ajey"
__revision__ = "1.0"	 

import re
import logging

#setup the prettify logger to log as required.
logger = logging.getLogger('prettify')


def singleton(class_name):
  """
  singleton decorator for all NumberPrettify class instances. 
    :param class_name The name of the class for which the singleton instance is required.
    :returns returns a new instance if no instance exists, else already existing one.
  """
  instances = {}
  def getinstance(*args, **kwargs):
    if class_name not in instances:
        instances[class_name] = class_name(*args, **kwargs)
    return instances[class_name]
  return getinstance

class PrettifyError(Exception):
    """
    This class is the error representation of the error for NumberPrettify functionality.
    """

    def __init__(self, value):
       self.value = value
    def __str__(self):
       return repr(self.value)

class PrettifyUtil(object):
    """
    This class provides utility methods which can be used by different implementations of
    the NumberPrettify classes.
    """

    @staticmethod
    def stripzeros(num_str):
       """
       All the leading zeros which are mathemically zero are removed. 
       Similarly all trailing zeros post the decimal point are removed as they shall not add value.
       """
       num_str = num_str.lstrip('0')
       num_str =  num_str.rstrip('0').rstrip('.') if '.' in num_str else num_str
       #Boundary cases
       #When numbers start with a decimal, so prepend a zero
       if num_str.startswith('.'): 
           num_str = "0%s" % num_str
       if num_str.endswith('.'): 
           num_str = num_str[:-1]
       if len(num_str) == 0:
           num_str = '0'
       return num_str

    @staticmethod
    def negativeNumber(num_str):
       """
       This method returns the number's sign and the absolute  value.
       """
       negative_num = False
       num_val = num_str
       if num_str[0] == '+' or  num_str[0] == '-':
          num_val = num_str[1:]
          if num_str[0] == '-':
             negative_num = True
       return negative_num, num_val

    @staticmethod
    def validateNumber(num_input):
       """
       The regular expression matches a valid numeric expression literally limited by the length of 
       the string. Python's long or double too donot have limit.
       """
       #[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?
       num_str = num_input.strip()
       if len(num_str):
           match = re.match(r"[+-]?\d*(\.\d+)?$", num_str)
           if match:
               return True
       logger.info("Invalid number for NumberPrettify :%s", num_input)
       raise PrettifyError("Invalid number for NumberPrettify")

class NumberPrettify(object):
    """
    The base class for representing large numbers in different formats. The representation algorithm can
    be implemented in the derived classes. An example of Shortscale large number representation has been
    included in the module.
    """
    def prettify(self, num_input):
       return num_input

@singleton
class Shortscale(NumberPrettify):
    """
    This class converts a given numeric type to shortscale large representation string. The input is expected
    to be string so the length of large numbers is not limited or get represented in exponential format.
    The shortscale converts all numbers greater that 6 digits (integer value without trailing zeros).
    """
    #The suffices for numbers with length 7 as M, 8 as M, 9 as M, 10 as B .... 13+ as T
    suffix = ['M','M','M','B','B','B','T']
    #This is not changing during runtime, might precalculate.
    suffix_length = len(suffix)
    #Minimum number of digits that shortscale  will convert.
    PRETTIFY_START = 6
    #The suffix to number of digits to be divided by.
    digits = {'M':6, 'B':9, 'T':12}

    def prettify(self, num_input):
       """
       The function works on the string representation of the number instead of numeric data type representation
       to allow large numbers with virtually unlimited length. Hence the number is converted to string representation.
       PrettifyUtil methods used to validate input and ready the input as per the required functionality.
       """
       if type(num_input) is str :
          num_str = num_input
       else:
          num_str = str(num_input)
       PrettifyUtil.validateNumber(num_str)
       negative_num, num_val = PrettifyUtil.negativeNumber(num_str)
       num_val = PrettifyUtil.stripzeros(num_val)
       #Split into integral and decimal parts, as our decision based on the number of digits on
       vals = num_val.split('.')
       #number of integral digits after removing all leading zeros.
       num_of_digits = len(vals[0])
       if num_of_digits > self.PRETTIFY_START:
          #Get the maximum suffix supported at this time.
          n_suffix = self.suffix[self.suffix_length - 1]
          #Adjust the index as the indices start from 0 for length 7 onwards.
          suffix_idx = num_of_digits - self.PRETTIFY_START - 1
          if suffix_idx <  self.suffix_length:
             n_suffix = self.suffix[suffix_idx]
          #Extract the required digits plus one decimal place.
          #NOTE: we are truncating not rounding, hence this should suffice.
          extract_num_digits = num_of_digits - self.digits[n_suffix] + 1
          val = vals[0][:extract_num_digits]
          #Better logic if large numbers require configurable number of places after decimal point.
          if val[-1] == '0':
             st =  "%s%s%s" % ('-' if negative_num else '',val[:-1],n_suffix)
          else:
             st = "%s%s.%s%s" % ('-' if negative_num else '',val[:-1],val[-1],n_suffix)
       else:
          st =  "%s%s" % ('-' if negative_num else '', num_val)
          if len(st) == 0:
              logger.info("The number has zero digits: %s",num_str)
              st = '0'

       return st

class PrettifyFactory():
    """
    Factory class to support multiple methods for representing large numbers. The factory supports
    shortscale at this point.
    """
    SHORTSCALE = 'SHORTSCALE'
    PRETTIFYTYPES = {SHORTSCALE: Shortscale}

    @staticmethod
    def getNumberPrettify(prettifyType):
        """
        Return the appropriate NumberPrettify. 
        Todo: Return the base class for the unsupported type instead of an exception. This is not a
        error scenario. The base prettify prints the number as is without modifications.
        """
        if prettifyType in PrettifyFactory.PRETTIFYTYPES:
           return PrettifyFactory.PRETTIFYTYPES[prettifyType]()
        logger.info("Unsupported NumberPrettify :%s" ,prettifyType)
        raise PrettifyError("Unsupported NumberPrettify format")

#If running as the main module.
if __name__ == "__main__":
    input_number = raw_input().strip()
    try:
        print PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE).prettify(input_number)
    except Exception as e:
        print e
