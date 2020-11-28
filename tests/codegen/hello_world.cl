class Main inherits IO {
   x : Int <- let x : Int <- 5, y : Int <- 4 in (x + y);

   y : Bool <- true;
   sqrt (x : Int) : Int
   {
        x * x
   };

   main(): IO {
       {
       (*while x < 10 loop{
       out_int(x);
       out_string("\n");
       x <- x + 1;
       } pool;*)
       case x of y : Int => y <- 10 ;esac;
       out_int(x);

       }
   };
};
