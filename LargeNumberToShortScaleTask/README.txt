This module consists a framework to represent/prettify large numbers in different
formats. The Shortscale format is supported.

#To run the task module.
python task.py 
32132432
32.1M

#To run the unit test cases for the module.
python test_unit_prettify.py 
test_base_class_print_unchanged (__main__.PrettifyTestCase)
Is base class prettify return the number unchanged ... ok
test_is_factory_returns_shortscale (__main__.PrettifyTestCase)
Is shortscale instance returned by the factory ... ok
test_is_number_sign_identified (__main__.PrettifyTestCase)
Is number sign identified correctly? ... ok
test_is_singleton_decorator (__main__.PrettifyTestCase)
Is singleton decorator for Shortscale class works? ... ok
test_is_trim_leading_zeros (__main__.PrettifyTestCase)
Is trimming leading zeros works? ... ok
test_is_trim_trailing_zeros (__main__.PrettifyTestCase)
Is trimming trailing zeros works? ... ok
test_is_trim_zeros_boundary_cases (__main__.PrettifyTestCase)
Is trimming trailing zeros works? ... ok
test_shortscale_conversion (__main__.PrettifyTestCase)
Is shortscale conversion for large numbers works? ... ok
test_validate_input (__main__.PrettifyTestCase)
Is input valid works? ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK

#To run the functional tests with different input and output.
python test_functional_prettify.py < test_functional_prettify.txt 
input: 1000000 , output: 1M , expected:  1M
input: 2500000.34 , output: 2.5M , expected:  2.5M
input: 532 , output: 532 , expected:  532
input: 1123456789 , output: 1.1B , expected:  1.1B
input: 00000000000 , output: 0 , expected:  0
input: 00 , output: 0 , expected:  0
input: , output: 'Invalid number for NumberPrettify' , expected: 'Invalid number for NumberPrettify'
input: 1234323453 , output: 1.2B , expected:  1.2B
input: +1234321543 , output: 1.2B , expected:  1.2B
input: -32142143121 , output: -32.1B , expected:  -32.1B
input: -000000321 , output: -321 , expected:  -321
input: +0000321412.1212000 , output: 321412.1212 , expected:  321412.1212
input: 321 , output: 321 , expected:  321
input: .1232  , output: 0.1232  , expected: 0.1232
input: 0.1232  , output: 0.1232  , expected: 0.1232
input: 11111110.1232  , output: 11.1M , expected: 11.1M
input: 12345.000 , output: 12345 , expected: 12345
input: 0000.0000 , output: 0 , expected: 0
