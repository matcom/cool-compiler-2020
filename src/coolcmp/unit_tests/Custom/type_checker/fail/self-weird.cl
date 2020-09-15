class Main {
    b : B <- b.fun(1);

    main() : SELF_TYPE { self };
};

class A {
    fun(n: Int) : SELF_TYPE {
        if n = 0 then
            new A
        else
            new B
        fi
    };
};

class B inherits A {};