-- The variables declared on each branch of a case must all have distinct types.

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

	test: A <- case 0 of
				b: Bool => new F;
				i: Bool => new E;
			esac;
};