-- Missing type

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test(a: A, b: Ball): Int { 4 };
};