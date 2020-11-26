class Main inherits IO {
   x : Int <- 1;

   sqrt (x : Int) : Int
   {
        x * x
   };

   main(): IO {
       {
       out_string("Hello, World (");
       out_int(x * 2);
       x <- 0 -7;
       x <- sqrt(x);
       out_string(", ");
       out_int(x);
        out_string(").\n");
       }
   };
};
