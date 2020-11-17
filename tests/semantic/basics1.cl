-- It is an error to redefine the IO class.

class IO {
	scan(): String { ":)" };
	print(s: String): IO { new IO };
};

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
};