-- A case-bound variable can shadow a same-named attribute.


class Main inherits Object
{
  var : String <- "bad";

  main() : Object
  {
    {
      case "good" of
	var : String =>
	  out_string( var );
      esac;

      out_string( "\n" );
    }
  };
};
