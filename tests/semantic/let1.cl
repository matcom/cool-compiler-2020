--The type of an initialization expression must conform to the declared type of the identifier.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	b: B <- let a: Bool, a: Int <- 5, a: String, a: A <- new F, b: B <- new E in b;
	test: B <- let a: Bool, a: Int <- 5, a: String, a: A <- new F, b: C <- new E in b;
}; 