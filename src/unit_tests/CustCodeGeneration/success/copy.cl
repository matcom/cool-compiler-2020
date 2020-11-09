class Main inherits IO {
    a : A <- new A;
    b : A;

    main() : SELF_TYPE {{
        if a = a.copy() then
            out_string("yes\n")

        else out_string("no\n") fi;

        b <- a.copy();

        out_int(a.getX());
        out_string("\n");

        out_int(b.getX());
        out_string("\n");

        b.setX(132);

        out_int(a.getX());
        out_string("\n");

        out_int(b.getX());
        out_string("\n");
    }};
};

class A {
    x:Int <- 5;
    getX() : Int { x };
    setX(value : Int) : Int { x <- value };
};