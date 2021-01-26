--The static type of an assignment is the static type of <expr>.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test(a: A): B { a <- new C };
	test2(a: A): D { a <- new C };
}; 
