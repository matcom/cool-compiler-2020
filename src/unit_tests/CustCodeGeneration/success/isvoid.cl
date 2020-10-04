class Main inherits IO {
    x : A;
    y : A <- new A;
    expr : Object;

    main() : SELF_TYPE {{
        if isvoid x then
            out_string("x is void\n")
        else
            out_string("x is not void\n")
        fi;

        if isvoid y then
            out_string("y is void\n")
        else
            out_string("y is not void\n")
        fi;

        let z:Int in expr <- while z < 3 loop z <- z + 1 pool;

        if isvoid expr then
            out_string("expr is void\n")

        else
            out_string("expr is not void\n")
        fi;
    }};
};

class A {};