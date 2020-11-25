class Main inherits IO {
    x : A <- new A;
    y : B <- new B;

    main(): SELF_TYPE {
        {
            y.fun(123);

            out_int(x.get_a());
            out_string("\n");

            out_int(y.get_a());
            out_string("\n");
        }
    };
};

class A {
    a : Int <- 5;

    get_a(): Int {
        a
    };
};

class B inherits A {
    fun(a : Int): Int {
        a <- a
    };
};