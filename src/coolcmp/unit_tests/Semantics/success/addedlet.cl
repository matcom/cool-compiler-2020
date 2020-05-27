class Foo {
	bar() : Int
	{
		let a:Int in a + let b:Int in b
	};
};

class Main {
	main() : Int {
		new Foo.bar()
	};
};