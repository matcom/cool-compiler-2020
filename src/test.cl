(*
<id>(<expr>,...,<expr>)  is shorthand for self.<id>(<expr>,...,<expr>).
*)

class A inherits Int {
	f(x: Int, y: Int): Int { x + y };
	g(x: Int): Int { x + x };
};
