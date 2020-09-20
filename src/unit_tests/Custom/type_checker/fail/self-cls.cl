class Main inherits IO {
    main() : SELF_TYPE {{
        out_int((new SELF_TYPE).f());
        out_string("\n");
        out_int((new SELF_TYPE).f());
        out_string("\n");
    }};
};

class A {
    f() : Int {5};
};

class B inherits A {
    f() : Int {7};
};