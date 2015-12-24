import unittest
from task import PrettifyFactory
from task import PrettifyUtil
from task import PrettifyError
from task import NumberPrettify
from task import Shortscale

class PrettifyTestCase(unittest.TestCase):
    """Tests for task.py."""

    def test_is_singleton_decorator(self):
        """Is singleton decorator for Shortscale class works?"""
        instance1 = PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE)
        instance2 = PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE)
        self.assertTrue((id(instance1)==id(instance2)), msg="Two instances are not the same, singleton decorator test failes.")

    def test_is_trim_leading_zeros(self):
        """Is trimming leading zeros works?"""
        self.assertTrue((PrettifyUtil.stripzeros('00001234') == '1234'), msg="Trimming leading zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('00001234.21') == '1234.21'), msg="Trimming leading zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('00001234.02100') == '1234.021'), msg="Trimming leading zeros from the input failed")

    def test_is_trim_trailing_zeros(self):
        """Is trimming trailing zeros works?"""
        self.assertTrue((PrettifyUtil.stripzeros('1234000') == '1234000'), msg="Trimming trailing zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('00001234.21000') == '1234.21'), msg="Trimming trailing zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('00001234.02100') == '1234.021'), msg="Trimming trailing zeros from the input failed")

    def test_is_trim_zeros_boundary_cases(self):
        """Is trimming trailing zeros works?"""
        self.assertTrue((PrettifyUtil.stripzeros('0.1234') == '0.1234'), msg="Trimming zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('1234.00') == '1234'), msg="Trimming zeros from the input failed")
        self.assertTrue((PrettifyUtil.stripzeros('0000.00') == '0'), msg="Trimming zeros from the input failed")

    def test_is_number_sign_identified(self):
        """Is number sign identified correctly?"""
        negative_num, _ = PrettifyUtil.negativeNumber('0.1234')
        self.assertFalse(negative_num, msg="Number sign identified correctly")
        negative_num, _ = PrettifyUtil.negativeNumber('-0.1234')
        self.assertTrue(negative_num, msg="Number sign identified correctly")
        negative_num, _ = PrettifyUtil.negativeNumber('+0.1234')
        self.assertFalse(negative_num, msg="Number sign identified correctly")

    def test_validate_input(self):
        """Is input valid works?"""
        self.assertRaises(PrettifyError, PrettifyUtil.validateNumber, '')
        self.assertRaises(PrettifyError, PrettifyUtil.validateNumber, 'invalid')
        self.assertTrue(PrettifyUtil.validateNumber('0.1234'), msg="Valid input number should return true")
        self.assertTrue(PrettifyUtil.validateNumber('+0.1234'), msg="Valid input number should return true")
        self.assertTrue(PrettifyUtil.validateNumber('-0.1234'), msg="Valid input number should return true")
        self.assertTrue(PrettifyUtil.validateNumber('00000.1234'), msg="Valid input number should return true")

    def test_base_class_print_unchanged(self):
        """Is base class prettify return the number unchanged"""
        self.assertTrue((NumberPrettify().prettify('0.1234') == '0.1234'), msg="Base Class prettify should return as is") 
        self.assertTrue((NumberPrettify().prettify('1234') == '1234'), msg="Base Class prettify should return as is") 
        self.assertTrue((NumberPrettify().prettify('0.000') == '0.000'), msg="Base Class prettify should return as is") 

    def test_shortscale_conversion(self):
        """Is shortscale conversion for large numbers works?"""
        numPrettify = PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE)
        self.assertTrue((numPrettify.prettify('1000000') == '1M'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('2500000.34') == '2.5M'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('532') == '532'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('1123456789') == '1.1B'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('00000000000') == '0'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('+1234321543') == '1.2B'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('-32142143121') == '-32.1B'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('-000000321') == '-321'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('+0000321412.1212000') == '321412.1212'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('.1232') == '0.1232'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('12345.000') == '12345'), msg="Shortscale number conversion as per algorithm")
        self.assertTrue((numPrettify.prettify('0000000.000') == '0'), msg="Shortscale number conversion as per algorithm")

    def test_is_factory_returns_shortscale(self):
        """Is shortscale instance returned by the factory"""
        numPrettify = PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE)
        #This will not work as the class has a decorator and it returns type(Shortscale) as function and will throw an error. 
        #self.assertIsInstance(numPrettify, Shortscale, msg="Factory with shortscale input should return that instance")
        self.assertTrue((numPrettify.__class__.__name__  == 'Shortscale'), msg="Factory with shortscale input should return that instance")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PrettifyTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
