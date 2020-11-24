(*
e0 .f(e1, . . . , en )
Assume e0 has static type A.
Class A must have a method f
the static type of the ith actual parameter must conform to the declared type of the ith formal parameter.
*)

class A inherits IO {
	f(x: Int, y: Int): Int { x + y };
	g(x: Int): Int { x + x };
};
class B inherits A {
	f(a: Int, b: Int): Int { a - b };
};
class C inherits B {
	ident(m: Int): Int { m };
	f(m: Int, n: Int): Int { m * n };
};
class D inherits B { 
	ident(v: String): IO { new IO.out_string(v) };
	f(v: Int, w: Int): Int { v / w };
	g(v: Int): Int { v + v + v };

	back(s: String): B { {
		out_string(s);
		self; 
	} };

	alphabet(a: A, b: B, c: C): D { self };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test: B <- new D.alphabet(new D, new D, new D.back("Hello ")).back("World!");
};