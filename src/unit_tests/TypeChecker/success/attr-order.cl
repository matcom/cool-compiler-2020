class Main inherits IO {
    a : Int <- b;
    b : Int <- 123;

    main(): SELF_TYPE {
        {
            out_int(a);
            out_string("\n");
            out_int(b);
            out_string("\n");
        }
    };
};