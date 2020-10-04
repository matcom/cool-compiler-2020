class Main inherits IO {
    x : Int;
    main() : SELF_TYPE {{
        x <- "asdasd7".length();
        out_int(x);
        out_string(x.type_name());
        out_string("\n");
    }};
};