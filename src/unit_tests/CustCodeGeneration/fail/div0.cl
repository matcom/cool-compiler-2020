class Main inherits IO {
    main() : SELF_TYPE {{
        out_string("fun");
        out_int(1231/0);
    }};
};