(*
The expression ~<expr> is the integer
complement of <expr>. The expression <expr> must have static type Int and the entire expression
has static type Int.
*)

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	test: Bool <- let x: Bool <- 1 / 2 - 3 + 4 < new A.type_name().concat(new B.type_name().concat(new C.type_name())).length()
				in ~new A.type_name().concat(new B.type_name().concat(new C.type_name())).length();
};