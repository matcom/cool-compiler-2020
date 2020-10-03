class Main inherits IO {
    x : Int <- 12;
    y : Int <- 17;

    main() : SELF_TYPE {{
        if x / 2 * 2 = x then
            out_int(1)
        else out_int(0) fi;

        if y / 2 * 2 = y then
            out_int(1)
        else out_int(0) fi;
    }};
};