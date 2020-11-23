class Main inherits IO {

    main () : Object {
        {
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
