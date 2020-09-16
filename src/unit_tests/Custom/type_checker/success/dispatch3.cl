class Main inherits IO {
    a : A;

    main(): String {
        a.f("str")
    };
};

class A {
    f(x: String) : String {x};
};

class B inherits A {};
class C inherits B {
    fun(x: Int) : Int {1};
};
