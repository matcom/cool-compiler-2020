import sys, lexerTest, parserTest

addr = None
addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)
