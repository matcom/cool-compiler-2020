class A{
   foo1: Int;
   bar1: String;
   f(a:Int): Int{a};

};

class D inherits C{
   foo1: Int;
   bar1: String;
   f(a:Int): Int{a};

};

class X{
   foo1: Int;
   bar1: String;
   f(a:Int): Int{a};

};

class Y inherits X{
  
};

class W inherits Y{
  
};

class B inherits A{
   foo2: Int;
   bar2: String;
   g(b: String): String{b}; 
};


class C inherits B{
   
   h(b: String): String{b}; 
};



class Main {
	main() : Int {
		1
	};
};
