class Hello {
   foo1: Int;
   bar1: String;
   f(a:Int): Int{a};

	

	
};

class World inherits Hello{
   foo2: Int;
   bar2: String;
   g(b: Hello): Hello{b}; 
};



class Main {
	main() : Int {
		1
	};
};
