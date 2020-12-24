<<<<<<< HEAD
<<<<<<< HEAD
import sys, lexerTest, parserTest
=======
import sys, lexerTest, parserTest, semanticTest
>>>>>>> semantic_work
=======
import sys, lexerTest, parserTest
>>>>>>> semantic_work

addr = None
addr = sys.argv[1]

lexerTest.run(addr)
parserTest.run(addr)
