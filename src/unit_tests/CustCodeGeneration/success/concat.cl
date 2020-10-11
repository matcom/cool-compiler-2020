class Main inherits IO {
    a : String <- "hello";
    main() : SELF_TYPE {{
        out_string(a.concat(" world!").concat("").concat("\n"));
        a <- a.concat("asd").concat("uasdh").concat("pulpa").concat("almendron\n");
        out_string(a);
        out_int(a.length());
        out_string("\n");
    }};
};