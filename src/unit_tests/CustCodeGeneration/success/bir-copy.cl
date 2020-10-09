class Main inherits IO {
    a : A <- new A;
    main() : SELF_TYPE {{
        if true.copy() = true then
            out_string("yes\n")
        else out_string("no\n") fi;

        if 5.copy() = 5 then
            out_string("yes\n")
        else out_string("no\n") fi;

        if a.copy() = a then
            out_string("yes\n")
        else out_string("no\n") fi;
    }};
};

class A {};