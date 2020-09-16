-- Case branches are tested from most specific to most generic.


class Main inherits IO
{
  main() : Object
  {
    let thing : Object in
      case thing of
        o : Object => out_string( "object\n" );
	      m : Main => out_string( "main\n" );
      esac
  };
};
