(*
The rule is
simple: If a class C inherits a method f from an ancestor class P, then C may override the inherited
definition of f provided the number of arguments, the types of the formal parameters, and the return
type are exactly the same in both definitions.
*)

class A {
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
	g(v: Int, w: Int, z: Int): Int { v + w + z };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
};