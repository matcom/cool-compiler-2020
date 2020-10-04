class Main inherits IO {
    main() : SELF_TYPE {{
        out_string(1.type_name());
        out_string("asd".type_name());
        out_string(new String);
        out_string(new String.type_name());
    }};
};