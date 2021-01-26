--The parent-child relation on classes defines a graph. This graph may not contain cycles.

class Main inherits IO {
	main(): IO { out_string("hi!") };

	main: IO <- out_string("bye!");
};

class A inherits B {
	x: Int <- 3;

	x(): String { ":)" };
};

class B inherits C {
	y: Int <- 2;

	div(a: Int, b: Int): Int { a / b};
};

class C inherits A { };