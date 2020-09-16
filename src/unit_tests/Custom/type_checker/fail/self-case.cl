class Main inherits IO {
    main(): SELF_TYPE {
        case "asd" of
            str : String => out_string(str);
            self : Object => out_string("is object");
        esac
    };
};