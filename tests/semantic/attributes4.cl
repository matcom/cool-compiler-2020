--Attributes are local to the class in which they are defined or inherited.

class A {
	a: Int <- 5;
};
class B inherits A {
	b: Bool <- true;
	test(x1: Int, y1: Int): Int {
		let x: Int <- x1, y: Int <-y1 in {
			x <- x + a;
			y <- y + a;
			if b then x + y else x - y fi;
		}
	};
};
class D inherits B {
	d: IO <- new Main.main();
	test3(x1: Int, y1: Int): IO {
		let x: Int <- x1, y: Int <-y1, c: String <- "C" in {
			x <- x + a;
			y <- y + a;
			if b then new IO.out_string(c) else d fi;
		}
	};
};
class C inherits B {
	c: String <- "C";
	test2(x1: Int, y1: Int): IO {
		let x: Int <- x1, y: Int <-y1 in {
			x <- x + a;
			y <- y + a;
			if b then new IO.out_string(c) else d fi;
		}
	};
};

class Main inherits IO {
	main(): IO { out_string("Hello World!") };
};