--The predicate must have static type Bool.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	i: Int <- 1;
	test: Object <- while "true" loop i <- i + 1 pool; 
};