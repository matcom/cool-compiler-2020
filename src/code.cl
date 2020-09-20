class A{
 x:Int <- 3;
};

class B inherits A {

};

class Main inherits IO {
	y:B <- new B;
	x:A <- y;

    main() : Object {{
		
		out_string("\n");
        if (x = y)
			then out_string("EQUAL\n")
			else out_string("NOT EQUAL\n")
		fi;
		out_string(x.type_name());
		out_string("\n");

		1 < 3 + let a:Int<-3 in a;
    }};
};
