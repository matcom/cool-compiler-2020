class Main inherits IO {
    a : A <- new A;

    main() : SELF_TYPE { out_int(a.fun(111, 222).getX()) };
};

class A inherits IO {
    x : Int <- 333;
    y : Int <- 444;

    getX() : Int {x};

    fun(x : Int, z: Int) : SELF_TYPE {{
        out_int(x);
        out_int(y);
        out_int(z);
    }};
};