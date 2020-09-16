class Main inherits IO {
    main() : IO {
	{
	    out_string((new Object).type_name().substr(4,1));
	    out_string( (isvoid (new Object)).type_name().substr(1,3) );
	    out_string("\n");
	}
    };
};
