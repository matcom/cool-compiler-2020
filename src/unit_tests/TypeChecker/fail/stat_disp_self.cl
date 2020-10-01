class Main inherits IO {
    a : A;

    main(): Int { a@SELF_TYPE.fun() };
};

class A {
    fun(): Int {1};
};