class Main {
    main(): SELF_TYPE { (new B).fun() }; --check associativity of new and dot
};

class A {
    a : SELF_TYPE <- fun();
    fun() : SELF_TYPE { new SELF_TYPE };
};

class B inherits A {};