class Main inherits IO {
     main() : String {
         foo(42)
     };

     foo(i : Int) : String {
        if i = 0 then "" else 
	    (let next : Int <- i / 10 in
		foo(next).concat(foo(i - next * 10))
	    )
        fi
    };
};