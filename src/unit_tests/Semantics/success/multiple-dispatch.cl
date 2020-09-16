class Main inherits IO {
  x : Int;
  f(y : Int) : Main { 
    {
      out_int(x + y);
      --out_string("\n");
      new Main;     --self;
    } 
  };
  
  g(z : Int) : Int { 
    {
      x <- x + 1;
      z + x;
    } 
  };

  main() : Object 
  {
    f(g(1)).f(g(g(5))).f(g(g(g(10))))
  };
};
