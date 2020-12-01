(*
<id>(<expr>,...,<expr>)  is shorthand for self.<id>(<expr>,...,<expr>).
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
	sum(m: Int, n: Int, p: Int): Int { m + n + p };
};
class D inherits B { 
	ident(v: String): IO { new IO.out_string(v) };
	f(v: Int, w: Int): Int { v / w };

	back(s: String): B { {
		out_string(s);
		g(2);
		sum(1, 2, 3);
		self; 
	} };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
};