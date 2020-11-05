(*
The rule is
simple: If a class C inherits a method f from an ancestor class P, then C may override the inherited
definition of f provided the number of arguments, the types of the formal parameters, and the return
type are exactly the same in both definitions.
*)

class A {
	f(x: Int, y: Int): Int { x + y };
};
class B inherits A {
	f(x: Int, y: Object): Int { x };
};
class C inherits B { };
class D inherits B { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
};