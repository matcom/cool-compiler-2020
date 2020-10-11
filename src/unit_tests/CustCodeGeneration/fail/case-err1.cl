class Main inherits IO {
    x : A <- new A;
    main() : Int {{
        -- out_string("fuk");
        case x of
            x : Int => "fun";
        esac;
        1;
    }};
};

class A {};