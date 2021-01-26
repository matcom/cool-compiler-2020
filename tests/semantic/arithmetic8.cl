 --The rules are exactly the same as for the binary arithmetic operations, except that the result is a Bool.

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	test: Int <- let x: Bool <- 1 / 2 - 3 + 4 < new A.type_name().concat(new B.type_name().concat(new C.type_name())).length()
				in 1 < new A.type_name().concat(new B.type_name().concat(new C.type_name())).length();
};
 
 
