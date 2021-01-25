(*
But it is an error to assign to self or to bind self in a let, a
case, or as a formal parameter. It is also illegal to have attributes named self.
*)

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test(self: IO): IO { self };
};
