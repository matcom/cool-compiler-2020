-- Missing type

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	test: F <- {
		new A;
		{ 
			new Ball;
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