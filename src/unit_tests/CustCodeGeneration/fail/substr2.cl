class Main inherits IO {
    st : Int;
    main() : SELF_TYPE {{
        st <- st - 1;
        out_string("abcdefg".substr(st, 9).concat("\n"));
    }};
};