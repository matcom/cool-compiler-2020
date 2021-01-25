(*
No method name may be defined multiple times in
a class, and no attribute name may be defined multiple times in a class, but a method and an attribute
may have the same name.
*)

class Main inherits IO {
	main(): IO { out_string("hi!") };

	main: IO <- out_string("bye!");
};

class A {
	x: Int <- 3;

	x(): String { "3" };

	x(): String { ":)" };
};