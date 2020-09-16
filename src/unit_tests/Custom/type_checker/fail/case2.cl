class Main inherits IO {
    main(): String {
        case "asd" of
            str : SELF_TYPE => out_string(str);
            bruh : Object => out_string("is object");
        esac
    };
};