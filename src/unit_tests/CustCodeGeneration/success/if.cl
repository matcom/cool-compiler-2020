class Main inherits IO {
    fun : Int;
    bigmain(z : String) : Int {{
        self;
        
        let x:Int <- 1, x:Int, x:Int <- x + 2, y:Int <- 5, x:Int <- 132, y:Int <- x + 2, wat:Int<-5 in {
            z <- case 1 of
                x : String => {"Hello"; out_string("asd"); };
                y : Object => {"Object"; out_string("branch other"); };
                fun : Main => {"Rock"; out_string("asasd"); };
                wat : Int => { x <- 123; out_int(wat); wat <- 11; out_string("is an int\n"); };
                res : IO => {res.type_name(); out_string("fuck");};
            esac.type_name();

            out_string("x=");
            out_int(x);
            out_string("\n");
            out_string("wat=");
            out_int(wat);
            out_string("\n");

            out_string(z);
            out_string("\n");

            let y : Int <- x + y, x : Int <- y in y;
        };
        1; 
    }};

    main() : Int {bigmain("Asd")};
};