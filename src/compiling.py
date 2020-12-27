import sys, lexerTest, parserTest, semanticTest

addr = None
addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)
semanticTest.run(addr)