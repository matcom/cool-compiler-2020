class Main inherits IO {
    a : Int <- b;
    b : Int <- 1 - 2;

    main() : SELF_TYPE {
        {
            out_string("a = "); out_int(a); out_string("\n");
            out_string("b = "); out_int(b); out_string("\n");
        }
    };
}; 