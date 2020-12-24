<<<<<<< HEAD
import sys, lexerTest, parserTest
=======
import sys, lexerTest, parserTest, semanticTest
>>>>>>> semantic_work

addr = None
addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)
<<<<<<< HEAD
=======
semanticTest.run(addr)
>>>>>>> semantic_work
