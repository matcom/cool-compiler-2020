class Main inherits IO {
   x : Int <- 1;
   main(): IO {
       {
       out_string("Hello, World (");
       out_int(3*2-7*2*2);
        out_string(").\n");
       }
   };
};
