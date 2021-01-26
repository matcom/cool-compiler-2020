--The static types of the two sub-expressions must be Int.

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	test: Int <- let x: Int <- 1 - 2 + 3 * 4 / new A.type_name().concat(new B.type_name().concat(new C.type_name())).length()
				in x <- x / new A.type_name().concat(new B.type_name().concat(new C.type_name()));
};