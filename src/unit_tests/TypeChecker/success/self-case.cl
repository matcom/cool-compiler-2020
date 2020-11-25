class Main inherits IO {
    main(): SELF_TYPE {
        case "asd" of
            str : String => out_string(str);
            bruh : Object => out_string("is object");
        esac
    };
};