class A inherits IO {
  b : Bool <- true;
  x : Int <- if b then 1 else ~1 fi;
  y : Int <- x + 3;
  z : Int <- y - 5;

  print_attr() : Object { {
   out_string("x: ");
   out_int(x);
   out_string("\nb: ");
   out_string(if b then "true" else "false" fi);
   out_string("\ny: ");
   out_int(y);
   out_string("\nz: ");
   out_int(z);
  } };
};

class Main {
  a : A <- new A;
  main() : Object {
    a.print_attr()
  };
};
