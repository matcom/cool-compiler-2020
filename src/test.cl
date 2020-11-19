class Main inherits IO {

    main () : Object {
        {
            let x:E <- new E in x.f() = x@E.f() ;
            let x:A <- new B in out_string( x.f().m() );
            let x:A <- new A in out_string( x.f().m() );
        }
        
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
