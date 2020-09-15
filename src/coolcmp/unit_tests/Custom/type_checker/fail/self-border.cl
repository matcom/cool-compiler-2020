class Main {
    main() : SELF_TYPE { self };
};

class A {
    fun() : SELF_TYPE { new A };
};

-- class B inherits A {};