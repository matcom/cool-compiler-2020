--For each branch, let Ti be the static type of <expri>. The static type of a case expression is Join 1≤i≤n Ti.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	b: B <- case "true" of
				i: Int => New C;
				b: Bool => New D;
				s: String => New E;
			esac;

	test: B <- case 0 of
				b: Bool => new F;
				i: Int => new E;
			esac;
};  
