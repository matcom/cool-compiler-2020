class Main {
    main(): Int {1};
};

class A {};

class B inherits A {
    a : C <- new SELF_TYPE;
};

class C inherits B {};