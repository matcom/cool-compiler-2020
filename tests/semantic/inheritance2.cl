--If C inherits from P, then P must have a class definition somewhere in the program.

class Main inherits IO {
	main(): IO { out_string("hi!") };

	main: IO <- out_string("bye!");
};

class Alo {
	x: Int <- 3;

	x(): String { "3" };
};

class B inherits A {
	div(a: Int, b: Int): Int { a / b};
	
	x: String <- "2";
};