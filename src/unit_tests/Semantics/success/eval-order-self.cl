-- The dispatched-upon object is evaluated after all actual arguments.


class Main inherits IO
{
  recite( value : Int ) : Main
  {
    {
      out_int( value );
      out_string( "\n" );
      new Main;
    }
  };

  disregard( a : Object ) : Object
  {
    new Main
  };

  main() : Object
  {
    recite( 2 ).disregard( recite( 1 ) )
  };
};
