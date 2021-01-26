--The parent-child relation on classes defines a graph. This graph may not contain cycles.

class Main inherits IO {
	main(): IO { out_string("hi!") };

	main: IO <- out_string("bye!");
};

class A inherits A {
	x: Int <- 3;

	x(): String { ":)" };
};