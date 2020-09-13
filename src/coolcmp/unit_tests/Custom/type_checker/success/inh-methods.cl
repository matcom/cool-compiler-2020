class Main inherits IO {
    b : B <- new B;
    a : A <- new A;

    main(): SELF_TYPE {
        {
            out_int(a.f(10));
            out_string("\n");
            out_int(b.f(10));
            out_string("\n");
        }
    };
};

class A {
    f(x: Int) : Int { x };
};

class B inherits A {
    f(x: Int) : Int { x + 1 };
};