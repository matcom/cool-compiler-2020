class Main inherits IO {
    x : Int <- 10;
    y : Bool <- true;
    z : Int <- 10;
    wa : Bool <- new Bool;

    main() : SELF_TYPE {{
        z <- z - 2 * z;
        out_int(~10);
        out_string("\n");
        out_int(~0);
        out_string("\n");
        out_int(~z);
        out_string("\n");

        if y then
            out_string("y true\n")
        else out_string("y false\n") fi;

        if not y then
            out_string("not y true\n")
        else out_string("not y false\n") fi;
        
        if not wa then
            out_string("not wa true\n")
        else out_string("not wa false\n") fi;
    }};
};