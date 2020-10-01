class Main {
    a : A <- a.fun();

    main() : Int { 1 };
};

class A {
    fun() : SELF_TYPE { new A };
};