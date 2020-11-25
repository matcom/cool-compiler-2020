class A {
	x:A;
	init():Object { x <- self };
	foo():Int { 1 };
	getx():A { x };
};

class B inherits A {
	foo():Int { 2 };
};

class Main inherits IO {
	main():Object {{
		let a:A <- new B in { 
			a.init();
			out_int(a.getx().foo());
		};
		out_string("\n");
	}};
};
