class Main inherits IO {
    a : A <- new A;
    b : B <- new B;
    c : C <- new C;

    main(): IO {
        {
            a@A.f("asd");
            b@B.f(1331);
            c@C.f(new IO);
        }
    };
};

class A {
    f(x: String) : String {x};
};

class B {
    f(x: Int) : Int {x};
};

class C {
    f(x: IO) : IO {x};
};