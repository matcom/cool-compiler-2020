import sys, lexerTest, parserTest, semanticTest, codegenTest

addr = None
addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)
semanticTest.run(addr)
codegenTest.run(addr)
