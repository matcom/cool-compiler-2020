--The type of let is the type of the body.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	b: B <- let a: Bool, a: Int <- 5, a: String, a: A <- new F, b: B <- new E in b;
	test: B <- let a: Bool, a: Int <- 5, a: String, a: A <- new F, b: A <- new E in b;
};