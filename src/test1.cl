class Main inherits IO {
   a : A;
  
   main(): IO { 
      out_string({
         case a of
            n : IO => "Hi";
            n : Object => "Hello";
         esac;
         a <- new A;
      })
   };
};

class A {
   i : Int;
   f(): Int {
      1
   };
};