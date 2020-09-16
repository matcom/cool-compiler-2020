class Main inherits IO {
    a : A;

    main(): Int {
        a.f("str")
    };
};

class A {
    f(x: String) : SELF_TYPE { self };
};