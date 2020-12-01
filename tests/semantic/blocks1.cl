--The static type of a block is the static type of the last expression.

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test: B <- {
		new A;
		{ 
			new B;
			{
				new C;
				{
					new D;
					{
						new E;
						{
							new F;
						};
					};
				};
			};
		};
	};
};