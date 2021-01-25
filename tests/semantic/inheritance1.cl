--It is illegal to redefine attribute names.

class Main inherits IO {
	main(): IO { out_string("hi!") };

	main: IO <- out_string("bye!");
};

class A {
	x: Int <- 3;

	x(): String { ":)" };
};

class B inherits A {
	x: Int;

	div(a: Int, b: Int): Int { a / b};
};