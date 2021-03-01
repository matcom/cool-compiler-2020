class Main inherits IO {
   a : String <- case 1 of
      n : Main => n.type_name();
      a : Int => a.type_name();
   esac;

   main(): IO {
	out_string(a)
   };
};
