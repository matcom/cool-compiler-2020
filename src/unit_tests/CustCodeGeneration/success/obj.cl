class Main inherits IO {
    a : A;
    b : B <- new B;
    c : A <- new A;
    d : B;
    main() : Object {{
        let x:A, y:B in if x = y then 0 else abort() fi;

        if a = b then
            out_string("yes\n")
        else out_string("no\n") fi;

        if c = d then
            out_string("yes\n")
        else out_string("no\n") fi;
    }};
};

class A{};
class B{};