class Main inherits IO {
    a : C <- new C;
    main() : SELF_TYPE {{
        out_int(a.f(111));
        out_int(a.f(222));
        out_int(a.fun(333, 444));
    }};
};

class A {
    f(x: Int) : Int { x };
};

class B inherits A {
    f(z : Int) : Int { z };
};

class C inherits B {
    fun(x: Int, y : Int) : Int { f(x) + f(y) };
};