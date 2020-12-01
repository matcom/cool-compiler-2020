--Attributes are local to the class in which they are defined or inherited.

class A {
	a: Int <- 5;
	test(x1: Int, y1: Int): Int {
		let x: Int <- x1, y: Int <-y1 in {
			x <- x + a;
			y <- y + a;
			if b then x + y else x - y fi;
		}
	};
};
class B inherits A {
	b: Bool <- true; 
};
class C inherits B {
	c: String <- "C"; 
};
class D inherits B {
	d: IO <- new Main.main();
};

class Main inherits IO {
	main(): IO { out_string("Hello World!") };
};