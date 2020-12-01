--evaluates to true if expr is void and evaluates to false if expr is not void.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	b: B <- if isvoid new F then 
				new C 
			else 
				if false then new D 
				else new E fi
			fi;

	test: B <- isvoid if isvoid new F then 
				new C 
			else 
				if false then new D 
				else new E fi
			fi;
}; 