class Main inherits IO {
    a : String <- "hello";
    main() : SELF_TYPE {{
        out_string(a.concat(" world!").concat("").concat("\n"));
        out_string(a.concat("asd").concat("uasdh").concat("pulpa").concat("almendron\n"));
    }};
};