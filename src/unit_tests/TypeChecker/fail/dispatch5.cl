class Main inherits IO {
    c : C;

    main(): Int {
        c@Object.f("str")
    };
};

class A {
    fu(x: String) : String {x};
};

class B inherits A {
    fa(): SELF_TYPE { self };
};

class C inherits B {
    fk(): Int { 1 };
};