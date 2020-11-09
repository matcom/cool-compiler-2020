class Main inherits IO {
    st : Int;
    main() : SELF_TYPE {{
        st <- st - 1;
        out_string("abcdefg".substr(0, st).concat("\n"));
    }};
};