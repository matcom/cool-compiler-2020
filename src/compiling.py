import sys, lexerTest, parserTest

addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)