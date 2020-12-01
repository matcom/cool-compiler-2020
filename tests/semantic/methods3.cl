--A formal parameter hides any definition of an attribute of the same name.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	a: C <- new C;
	test(a: D): D { a };
	test2(a: B): C { a };
};