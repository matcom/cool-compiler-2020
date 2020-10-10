class Main inherits IO {
    a : String;

    main() : SELF_TYPE {{
        a <- "hello world!";
        out_string(a.copy());

        a <- "asdasdasdsaasdasd\n";
        out_string(a.copy());

        a <- "";
        out_string(a.copy());

        a <- "\n";
        out_string(a.copy());
    }};
};