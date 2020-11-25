class Main inherits IO {
    main() : SELF_TYPE {{
        if "" = "" then
            out_string("yes\n")
        else out_string("no\n") fi;
        
        if "hola" = "holaa" then
            out_string("yes\n")
        else out_string("no\n") fi;
        
        if "a" = "a" then
            out_string("yes\n")
        else out_string("no\n") fi;

        if "a" = "ab" then
            out_string("yes\n")
        else out_string("no\n") fi;

        if "ab" = "a" then
            out_string("yes\n")
        else out_string("no\n") fi;

        if "" = "abasdsd" then
            out_string("yes\n")
        else out_string("no\n") fi;

        if "asdasdsd" = "" then
            out_string("yes\n")
        else out_string("no\n") fi;

        if "\n" = "\n" then
            out_string("yes\n")
        else out_string("no\n") fi;
    }};
};