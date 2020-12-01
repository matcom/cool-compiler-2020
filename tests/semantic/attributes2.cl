--The static type of the expression must conform to the declared type of the attribute.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	test1: IO <- new Main;
	test2: C <- new D;

	main(): IO { out_string("Hello World!")};
};