class Main {
    main(): SELF_TYPE { self };
};

class A {
    a : SELF_TYPE <- fun();
    fun() : SELF_TYPE { new SELF_TYPE };
};

class B inherits A {};