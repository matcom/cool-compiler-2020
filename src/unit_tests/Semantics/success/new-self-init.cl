-- new SELF_TYPE creates an object with the same dynamic type as self,
-- which affects initialization of the new object's attributes.


class Base inherits IO
{
  baseAttr : Int <- {report(1); 1;};

  report( value : Int ) : Base
  {
    {
      out_int( value );
      out_string( "\n" );
      self;
    }
  };

  duplicate() : Base
  {
    --new SELF_TYPE
    self
  };
};


class Derived inherits Base
{
  derivedAttr : Int <- {report(2); 2;};

  report( value : Int ) : Base
  { 
    {
      out_string("old: ");
      out_int(derivedAttr);
      out_string(".  new: ");
      derivedAttr <- value;
      self@Base.report( derivedAttr );
    }
  };
};


class Main 
{
  main() : Object
  {
    (new Derived).report ( 5 )
	.duplicate().report ( 29 )
  };
};
