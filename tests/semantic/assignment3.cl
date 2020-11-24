--The static type of an assignment is the static type of <expr>.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	a: A;
	b: B <- a <- new C;
	d: D <- a <- new C;
}; 
