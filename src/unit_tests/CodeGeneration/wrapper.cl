
class Main inherits IO {

  f(x:Int) : Object {{
    --x;
    --(new Object);
    --(new Object).type_name()
    --(new Object).type_name().length()
    --(new Object).type_name().length() = 2;
    (new Object).type_name().length() = 2;
  }};

  main():Object {{

    out_string(f(2).type_name());

  }};
};