class Foo {
	bar(b:Int <- 10):Int {
		{
			let a:Int in (a + b);
			(let a:Int in a) + b;
			let a:Int in (a) + (b);
		}
	};
};

class Main {
	main() : Int {
		1
	};
};