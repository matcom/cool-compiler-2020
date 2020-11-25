class Main inherits IO {
    fun : Int;
    bigmain(z : Int) : Int {{
        self;

        out_int(fun);
        out_int(z);
        
        let x:Int <- 1, x:Int, x:Int <- x + 2, y:Int <- 5, x:Int <- 132, y:Int <- x + 2, z:Int <- fun in {
            out_int(x);
            out_int(y);
            out_int(z);
            x <- 132;
            out_int(x);
            let y : Int <- x + y, x : Int <- y in {
                y;
                out_int(y);
                let x:Int <- x + z + y, y:Int <- y+y+z+x+fun, z :Int <- x+y in {
                    out_int(x);
                    out_int(y);
                    out_int(z);
                    out_int(fun);
                };

                out_int(x);
            };

            out_int(x);
            out_int(y);
            out_int(z);
        };
        1;
    }};

    main() : Int {bigmain(321)};
};

class A inherits Main {
    q : SELF_TYPE;

    f(fu: Int) : Int { {self; fun; q; fu;}};
};