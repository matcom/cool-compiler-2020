(*
The expression not <expr> is the boolean complement of <expr>. The expression
<expr> must have static type Bool and the entire expression has static type Bool.
*)

class A { };
class B inherits A { };
class C inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
	test: Int <- let x: Bool <- 1 / 2 - 3 + 4 < new A.type_name().concat(new B.type_name().concat(new C.type_name())).length()
				in not 1 < new A.type_name().concat(new B.type_name().concat(new C.type_name())).length();
};