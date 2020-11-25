-- Test of Object.copy

class Base inherits IO
{
  b : Base;
  baseAttr : Int <- {report(1); 1;};

  report( value : Int ) : Base
  {
    {
      out_int( value );
      out_string( "\n" );
      b;
    }
  };

  duplicate() : Base
  {
    b
  };
};


class Derived inherits Base
{
  d : Derived;
  derivedAttr : Int <- {report(2); 2;};

  report( value : Int ) : Base
  { 
    {
      out_string("old: ");
      out_int(derivedAttr);
      out_string(".  new: ");
      derivedAttr <- value;
      d@Base.report( derivedAttr );
    }
  };
};


class Main 
{
  main() : Object
  {
    (new Derived).report(5).duplicate().report(29)
  };
};
