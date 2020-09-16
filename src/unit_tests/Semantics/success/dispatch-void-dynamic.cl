-- Dynamically dispatching on a void object is a runtime error.


class Main inherits IO
{
  main() : IO
  {
    let nothing : Object <- while false loop 1 pool in
      out_string(nothing.type_name())
  };
};
