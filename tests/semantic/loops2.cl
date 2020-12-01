--The static type of a loop expression is Object.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	i: Int <- 1;
	test: Object <- while not false loop i <- i + 1 pool; 
	test2: Int <- while not false loop i <- i + 1 pool; 
}; 
