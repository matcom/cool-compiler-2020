class Main inherits IO {
    a : B <- new B;
    main() : SELF_TYPE {
        {
            out_int(a.get_a());
            out_string("\n");
        }
    };
};

class A {
    a : Int <- 5;
};

class B inherits A {
    a : Int;
    get_a(): Int {
        a
    };
};