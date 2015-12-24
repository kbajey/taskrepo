from task import PrettifyFactory

number_test_cases = int(raw_input().strip())
for each_case in xrange(number_test_cases):
    input_number, expected_output = raw_input().strip().split(',')
    numberFactory =  PrettifyFactory.getNumberPrettify(PrettifyFactory.SHORTSCALE)
    try:
        print "input: %s , output: %s , expected: %s" % (input_number, numberFactory.prettify(input_number),expected_output)
    except Exception as e:
        print "input: %s, output: %s , expected: %s" % (input_number, e, expected_output)
