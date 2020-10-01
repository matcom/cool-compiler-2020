class Main inherits IO {
    a : A;

    main(): A {
        a.f("str")
    };
};

class A {
    f(x: String) : SELF_TYPE { self };
};