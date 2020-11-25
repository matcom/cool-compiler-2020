class Main { main(): Int {1}; };

class A {
    fun() : SELF_TYPE { new SELF_TYPE };
};

class B inherits A {
    b : SELF_TYPE <- fun();
};