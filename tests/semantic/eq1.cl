(*
The comparison = is a special
case. If either <expr1> or <expr2> has static type Int, Bool, or String, then the other must have the
same static type. Any other types, including SELF TYPE, may be freely compared.
*)

class A { };
class B inherits A { };

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	x: Bool <- 1 = 2;
	test: Bool <- 1 = new A;
	y: Bool <- "1" = "2";
	z: Bool <- true = not false;
};  