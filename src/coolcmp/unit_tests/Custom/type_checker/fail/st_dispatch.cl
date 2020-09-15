class Main inherits IO {
    a : A <- new A;
    b : B <- new B;
    c : C <- new C;

    main(): Int {
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

class C inherits Main {
    f(x: IO) : SELF_TYPE { new SELF_TYPE };
};