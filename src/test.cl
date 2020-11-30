class Main inherits IO {

    main () : Object {
        "H"
    };
};

class A {
    m () : String { "A" };
    f () : A { new A };
};

class B inherits A {
    m () : String { "B" };
};


class C {
 f () : String {"C"};
};

class D inherits C {
};

class E inherits D {
 f () : String {"E"};
};
