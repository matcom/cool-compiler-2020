class Hello {

   foo:Int <- 89;
   bar:Int;
   o:Int <- 3*2+8;
   j:Int <- 1+5;

   gog() :Bool {
      true
   };

   gog2() :Int {
      o <- 221
   };
   
   foo(a:Int, b:Int, c:String, o:Int): Int  {{
      a <- 2*7+8;
      b <- 1*2*3*4;
   }};
   
   bar() :Int {
      6*2
   };
   
};


class Adios {
   a:Int <- 90;
};


class Hola inherits Adios {
   b:Int <- 90;
};

class Main {
	main() : Int {
		1
	};
};