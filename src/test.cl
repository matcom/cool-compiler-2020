class Main
{
   a : Int <- 2;
   main():Object
   {
      3+4+a
   };
};

class A
{
	x:Int;

   suma (a:Int, b:Int) : Int
   {
      {
      let x:Int <- 3, a : String in
      {
         a;
      };
      x;
      }

   };
     
   resta (a:Int, b:Int) :Int
   {
      let b : B <- new B in 
      {
         b.suma(a,a);
      }
   };
	
};

class B inherits A
{
   y: Int <- let c:Int <- 2, d:Int <-3 in c+d;
   
   suma ( a: Int, b: Int) : Int
   {
      a
   };
};