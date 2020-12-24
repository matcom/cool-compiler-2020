(*
e@B.f() invokes the method
f in class B on the object that is the value of e. For this form of dispatch, the static type to the left of
“@”must conform to the type specified to the right of “@”.
*)

class A {
	f(x: Int, y: Int): Int { x + y };
	g(x: Int): Int { x + x };
};
class B inherits A {
	f(a: Int, b: Int): Int { a - b };
	sum(m: Int, n: Int, p: Int): Int { m + n + p };
};
class C inherits B {
	ident(m: Int): Int { m };
	f(m: Int, n: Int): Int { m * n };
};
class D inherits B { 
	ident(v: String): IO { new IO.out_string(v) };
	f(v: Int, w: Int): Int { v / w };
	g(v: Int): Int { v + v + v };
	sum(v: Int, w: Int, z: Int): Int { v - w - z };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	a: A <- new D;
	b: Int <- new D@B.sum(1, 2, 3);
	test: Int <- a@B.sum(1, 2, 3);
}; 
