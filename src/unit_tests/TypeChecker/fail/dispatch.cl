class Main inherits IO {
    a : A;

    main(): Int {
        a.f(1, "str")
    };
};

class A {
    f(x: Int, y: Int) : Int { x };
};
