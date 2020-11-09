class Main inherits IO {
    a : A <- new A;
    b : A;
    main() : SELF_TYPE {{
        a.setX();

        b <- a.copy();

        out_int(a.getX());
        out_string("\n");
        out_int(b.getX());
        out_string("\n");

        out_string(a.getY());
        out_string(b.getY());
    }};
};

class A inherits IO {
    x : Int <- 7;
    y : String <- fun();
    z : Bool;
    a : Int <- 5;

    getY() : String {y};

    fun() : String {{
        out_string("initialized!\n");
        "hola";
    }};

    getX() : Int {x};
    setX() : Int {x<- 312};
};