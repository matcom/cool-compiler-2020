class Main inherits IO {
    a : C <- new C;
    main() : SELF_TYPE {
        out_int(a.fun(333, 444))
    };
};

class C {
    fun(x: Int, y : Int) : Int { x + y };
};