class A{
 x:Int <- 3;
};

class B inherits A {

};

class Main inherits IO {
	y:B <- new B;
	x:A <- y;

    main() : Object {{
		
		out_int(0);
        if (x = y)
			then out_int(1)
			else out_int(2)
		fi;
		
		out_int(0);

		1 < 3 + let a:Int<-3 in a;
    }};
};
