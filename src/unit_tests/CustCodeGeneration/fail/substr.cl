class Main inherits IO {
    st : Int <- 5;
    main() : Int {{
        st <- st - 6;
        out_string("abcdefg".substr(3, 2).concat("\n"));
        out_string("abcdefg".substr(0, 0).concat("\n"));
        out_string("abcdefg".substr(0, 1).concat("\n"));
        out_string("abcdefg".substr(0, st).concat("\n"));
        1;
    }};
};